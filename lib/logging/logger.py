from lib.logging.rotate_when import RotateWhen
from lib.settings import settings
from lib.utils.python import (
    select_value_no_default,
    get_caller_filename,
    get_caller_name,
    get_caller_lineno,
)
import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from pythonjsonlogger import jsonlogger


class Logger:

    CALLER_INFO_DEPTH = 4

    def __init__(
        self,
        logfile: str | Path = None,
        level: str = None,
        rotate_interval: int = None,
        rotate_when: str = None,
        backup_count: int = None,
    ):
        # handle default values
        self.when = rotate_when
        self.interval = rotate_interval
        self.backup_count = backup_count

        self.log_level = select_value_no_default(level, settings.logging.level)
        self.logger = select_value_no_default(logfile, settings.logging.path)

    @property
    def caller_info(self):
        depth = self.CALLER_INFO_DEPTH
        return {
            "file": get_caller_filename(depth),
            "function": get_caller_name(depth),
            "line_number": get_caller_lineno(depth),
        }

    def debug(self, msg, **kwargs):
        self.logger.debug(msg, extra={**kwargs, **self.caller_info})

    def info(self, msg, **kwargs):
        self.logger.info(msg, extra={**kwargs, **self.caller_info})

    def warning(self, msg, **kwargs):
        self.logger.warning(msg, extra={**kwargs, **self.caller_info})

    def error(self, msg, **kwargs):
        self.logger.error(msg, extra={**kwargs, **self.caller_info})

    def critical(self, msg, **kwargs):
        self.logger.critical(msg, extra={**kwargs, **self.caller_info})

    @property
    def logfile(self):
        return self._logfile

    @property
    def when(self):
        return self._when

    @when.setter
    def when(self, value):
        self._when = select_value_no_default(value, settings.logging.rotate_when)

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = select_value_no_default(
            value, int(settings.logging.rotate_interval)
        )

    @property
    def backup_count(self):
        return self._backup_count

    @backup_count.setter
    def backup_count(self, value):
        self._backup_count = value

    @property
    def log_level(self):
        if not hasattr(self, "_log_level"):
            return None
        return self._log_level.upper()

    @log_level.setter
    def log_level(self, level):
        assert level.upper() in logging._nameToLevel
        self._log_level = level.upper()
        if self.logger:
            self.logger.setLevel(logging._nameToLevel[level])

    @property
    def logger(self):
        if not hasattr(self, "_logger"):
            return None
        return self._logger

    @logger.setter
    def logger(self, logfile):
        self._logfile = logfile
        self._logger = logging.getLogger(logfile)
        if self.log_level:
            self._logger.setLevel(logging._nameToLevel[self.log_level])
        self.add_file_handler()
        self.add_stream_handler()

    def add_stream_handler(self):
        self._stream_handler = StreamHandler()
        self._stream_handler.setFormatter(
            jsonlogger.JsonFormatter(
                self.format_string,
                rename_fields=self.renamed_fields,
                json_indent=self.stream_json_indent,
            )
        )
        self._logger.addHandler(self._stream_handler)

    def add_file_handler(self):

        self._file_handler = TimedRotatingFileHandler(
            filename=self.logfile,
            when=RotateWhen(self.when).value,
            interval=self.interval,
            backupCount=self.backup_count,
        )
        self._file_handler.setFormatter(
            jsonlogger.JsonFormatter(
                self.format_string,
                rename_fields=self.renamed_fields,
            )
        )
        self._logger.addHandler(self._file_handler)

    @property
    def format_string(self):
        return "%(name)s %(asctime)s %(levelname)s %(process)d %(message)s"

    @property
    def renamed_fields(self):
        return settings.logging_renamed_fields.to_dict()

    @property
    def stream_json_indent(self):
        return int(settings.logging.stream_json_indent)
