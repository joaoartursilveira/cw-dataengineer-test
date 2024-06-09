import os
import logging
from pathlib import Path


class Config:

    LOG_FILE = Path('app/database/log/output.log')
    LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'


class Logger:

    """
    Used for logging.
    """

    def __init__(self, log_type):
        """
        Constructor function
        :param:

        log_type: type of log(database or webcrawler vs.)
        """

        self.log_type = log_type
        self.log_dir = Config.LOG_FILE.parent
        self.log_file = Config.LOG_FILE
        self.log_format = Config.LOG_FORMAT
        self.close_log()
        self.logger = self.get_log_config()

    def debug(self, msg: str) -> None:
        if self.logger is not None:
            self.logger.debug("{}".format(msg))

    def info(self, msg: str) -> None:
        if self.logger is not None:
            self.logger.info("{}".format(msg))

    def warning(self, msg: str) -> None:
        if self.logger is not None:
            self.logger.warning("{}".format(msg))

    def error(self, msg: str) -> None:
        if self.logger is not None:
            self.logger.error("{}".format(msg))

    def critical(self, msg: str) -> None:
        if self.logger is not None:
            self.logger.critical("{}".format(msg))

    def get_log_config(self) -> logging.Logger:
        """
        Configuration for logging
        :return:
        """

        self.log_dir.mkdir(parents=False, exist_ok=True)

        # create logger
        logger = logging.getLogger(self.log_type)
        # create handler
        file_path = os.path.abspath(self.log_file)
        handler = logging.FileHandler(file_path)
        # create formatter
        formatter = logging.Formatter(self.log_format)
        # set Formatter
        handler.setFormatter(formatter)
        # add handler
        logger.addHandler(handler)
        # set level
        logger.setLevel(logging.INFO)

        return logger

    def close_log(self) -> None:
        """
        Remove all logger
        :return: None
        """

        logger = logging.getLogger(self.log_type)
        while logger.hasHandlers():
            logger.removeHandler(logger.handlers[0])
