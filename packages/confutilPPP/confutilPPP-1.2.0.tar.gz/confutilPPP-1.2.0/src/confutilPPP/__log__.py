import logging
import sys


def _reset_logger(log):
    FMT = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s'
    DATE_FMT = "%Y-%m-%d %H:%M:%S"
    for handler in log.handlers:
        handler.close()
        log.removeHandler(handler)
        del handler
    log.handlers.clear()
    log.propagate = False
    console_handle = logging.StreamHandler(sys.stdout)
    console_handle.setFormatter(
        logging.Formatter(
            fmt=FMT,
            datefmt=DATE_FMT
        )
    )
    file_handle = logging.FileHandler("confutilPPP.log", encoding="utf-8")
    file_handle.setFormatter(
        logging.Formatter(
            fmt=FMT,
            datefmt=DATE_FMT
        )
    )
    log.addHandler(file_handle)
    log.addHandler(console_handle)


def _get_logger():
    log = logging.getLogger("confutilPPP")
    _reset_logger(log)
    log.setLevel(logging.INFO)
    return log


# 日志句柄
logger = _get_logger()
