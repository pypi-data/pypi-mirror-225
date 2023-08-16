import logging
import re
import os
import sys
from contextlib import contextmanager


@contextmanager
def suppress_std():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull

        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


class Formatter(logging.Formatter):
    grey = "\x1b[38;20m"
    cyan = "\x1b[36;20m"
    purple = "\x1b[35;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # format = "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    format = "[%(name)s] | %(levelname)s -> %(message)s"

    FORMATS = {
        logging.DEBUG: f"{purple}{format}{reset}",
        logging.INFO: f"{cyan}{format}{reset}",
        logging.WARNING: f"{yellow}{format}{reset}",
        logging.ERROR: f"{red}{format}{reset}",
        logging.CRITICAL: f"{bold_red}{format}{reset}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def mklog(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    for handler in logger.handlers:
        logger.removeHandler(handler)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(Formatter())
    logger.addHandler(ch)

    # Disable log propagation
    logger.propagate = False

    return logger
