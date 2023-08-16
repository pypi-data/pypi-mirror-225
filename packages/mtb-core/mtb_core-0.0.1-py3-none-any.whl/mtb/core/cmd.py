import subprocess
from pathlib import Path
import threading
from queue import Queue, Empty
import signal
from contextlib import suppress


def enqueue_output(out, queue):
    for line in iter(out.readline, b""):
        queue.put(line)
    out.close()


def run_command(cmd):
    if isinstance(cmd, str):
        shell_cmd = cmd
    elif isinstance(cmd, list):
        shell_cmd = ""
        for arg in cmd:
            if isinstance(arg, Path):
                arg = arg.as_posix()
            shell_cmd += f"{arg} "
    else:
        raise ValueError(
            "Invalid 'cmd' argument. It must be a string or a list of arguments."
        )

    process = subprocess.Popen(
        shell_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
    )

    # Create separate threads to read standard output and standard error streams
    stdout_queue = Queue()
    stderr_queue = Queue()
    stdout_thread = threading.Thread(
        target=enqueue_output, args=(process.stdout, stdout_queue)
    )
    stderr_thread = threading.Thread(
        target=enqueue_output, args=(process.stderr, stderr_queue)
    )
    stdout_thread.daemon = True
    stderr_thread.daemon = True
    stdout_thread.start()
    stderr_thread.start()

    interrupted = False

    def signal_handler(signum, frame):
        nonlocal interrupted
        interrupted = True
        print("Command execution interrupted.")

    # Register the signal handler for keyboard interrupts (SIGINT)
    signal.signal(signal.SIGINT, signal_handler)

    # Process output from both streams until the process completes or interrupted
    while not interrupted and (
        process.poll() is None or not stdout_queue.empty() or not stderr_queue.empty()
    ):
        with suppress(Empty):
            stdout_line = stdout_queue.get_nowait()
            if stdout_line.strip() != "":
                print(stdout_line.strip())
        with suppress(Empty):
            stderr_line = stderr_queue.get_nowait()
            if stderr_line.strip() != "":
                print(stderr_line.strip())
    return_code = process.returncode

    if return_code == 0 and not interrupted:
        print("Command executed successfully!")
    else:
        if not interrupted:
            print(f"Command failed with return code: {return_code}")
