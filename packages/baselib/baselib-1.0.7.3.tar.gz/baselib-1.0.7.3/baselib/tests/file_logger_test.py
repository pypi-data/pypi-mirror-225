# -*- coding:utf-8 -*-
from baselib.log import file_logger
import logging


class TestFileLogger:
    test_obj = file_logger()

    def test_default_log_level(self):
        assert self.test_obj.level == logging.DEBUG

    def test_default_log_format(self):
        formatter = logging.Formatter(
            '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d-%(module)s] %(message)s')
        assert self.test_obj.handlers[0].formatter._fmt == formatter._fmt

    def test_default_time_rotating(self):
        assert isinstance(self.test_obj.handlers[0], logging.FileHandler)

    def test_no_rotating(self):
        test_obj = file_logger(time_rotating=None)
        test_obj.info("no time rotating")

    def test_custom_name(self):
        logger = file_logger(name='test')
        assert logger.name == 'test'

    def test_custom_log_level(self):
        logger = file_logger(log_level='WARNING')
        assert logger.level == logging.WARNING

    # def test_custom_log_format(self):
    #     log_format = '[%(asctime)s] %(message)s'
    #     logger = file_logger(log_format=log_format)
    #     formatter = logging.Formatter(log_format)
    #     assert logger.handlers[0].formatter._fmt == formatter._fmt

    # def test_time_rotating_Daily_rotation_interval(self):
    #     handler_class, interval, backup_count, delay, utc, at_time, encoding \
    #         = type(file_handler), 'D', 0, False, False, None, 'utf-8'
    #     handler_instance = handler_class(
    #         filename=log_path,
    #         when=interval,
    #         backupCount=backup_count,
    #         delay=delay,
    #         utc=utc,
    #         atTime=at_time,
    #         encoding=encoding
    #     )
    #     assert isinstance(
    #         handler_instance,
    #         TimedRotatingFileHandler) and handler_instance.when == 'D'
