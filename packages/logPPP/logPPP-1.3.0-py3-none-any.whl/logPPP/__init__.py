import logging
import os
import sys
from logging import *

__all__ = ['__version__', 'get_logger', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NOTSET', 'FATAL',
           'WARN']
__version__ = '1.3.0'


def get_logger(logging_level=None, logging_is_output_sys_stdout=None,
               logging_file=None, logger_name=None, logging_fmt=None, logging_date_fmt=None):
    # 配置
    _LOGGING_LEVEL = logging.INFO
    _LOGGING_IS_OUTPUT_SYS_STDOUT = True
    _LOGGING_IS_OUTPUT_FILE = False
    _LOGGING_FILE = os.path.join(os.getcwd(), "log.log")
    _LOGGER_NAME = os.path.splitext(os.path.basename(_LOGGING_FILE))[0]
    _LOGGING_FMT = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s'
    _LOGGING_DATE_FMT = '%Y-%m-%d %H:%M:%S'

    if logging_level is not None:
        _LOGGING_LEVEL = logging_level

    if logging_is_output_sys_stdout is not None:
        _LOGGING_IS_OUTPUT_SYS_STDOUT = logging_is_output_sys_stdout

    if logging_file is not None:
        # 如果是相对路径，则转换为绝对路径
        if not os.path.isabs(logging_file):
            logging_file = os.path.abspath(logging_file)
        _LOGGING_FILE = logging_file
        _LOGGER_NAME = os.path.splitext(os.path.basename(_LOGGING_FILE))[0]
        _LOGGING_IS_OUTPUT_FILE = True

    if logger_name is not None:
        _LOGGER_NAME = logger_name

    if logging_fmt is not None:
        _LOGGING_FMT = logging_fmt

    if logging_date_fmt is not None:
        _LOGGING_DATE_FMT = logging_date_fmt

    logger_ = logging.getLogger(_LOGGER_NAME)
    for h in logger_.handlers:
        h.close()
        logger_.removeHandler(h)
        del h
    logger_.handlers.clear()
    logger_.propagate = False
    logger_.setLevel(_LOGGING_LEVEL)

    if _LOGGING_IS_OUTPUT_SYS_STDOUT:
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(logging.Formatter(_LOGGING_FMT, datefmt=_LOGGING_DATE_FMT))
        logger_.addHandler(ch)

    if _LOGGING_IS_OUTPUT_FILE:
        fh = logging.FileHandler(_LOGGING_FILE, encoding='utf-8')
        fh.setFormatter(logging.Formatter(_LOGGING_FMT, datefmt=_LOGGING_DATE_FMT))
        logger_.addHandler(fh)
    return logger_
