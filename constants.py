import logging
import coloredlogs


CONSOLE_FORMATTER = coloredlogs.ColoredFormatter(
    fmt=(
            "%(asctime)s.%(msecs)03d [%(filename)s:%(lineno)d %(name)s.%(funcName)s()] "
            "[%(levelname)s]: %(message)s"
        ),
    datefmt="%Y-%m-%d %H:%M:%S",
    level_styles=coloredlogs.DEFAULT_LEVEL_STYLES,
)
DEFAULT_LOG_FILE = "./logs/diff_bolder.log"
DEFAULT_LOG_LEVELS = {
    "file_loglevel": "DEBUG",
    "console_loglevel": "DEBUG",
}
DESIRED_EXTENSIONS = ["docx", "fdx"]
FORMATTER = logging.Formatter(
    (
        "%(asctime)s.%(msecs)03d [%(filename)s:%(lineno)d %(name)s.%(funcName)s()] "
        "[%(levelname)s]: %(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOG_LEVELS = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "WARN": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0,
}
