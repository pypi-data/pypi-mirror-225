import logging

from educommon.logger.helpers import (
    get_logger_method,
)
from educommon.logger.loggers import (
    WebEduLogger,
)


default_app_config = 'educommon.logger.apps.EduLoggerConfig'

# Переопределение класса логера
logging.setLoggerClass(WebEduLogger)

__all__ = ['debug', 'info', 'error', 'warning', 'default_app_config']


debug = get_logger_method(level='DEBUG')
info = get_logger_method(level='INFO')
error = get_logger_method(level='ERROR')
warning = get_logger_method(level='WARNING')
