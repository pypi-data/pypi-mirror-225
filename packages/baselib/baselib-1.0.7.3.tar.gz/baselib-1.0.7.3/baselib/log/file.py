# -*- coding:utf-8 -*- 
import logging
import logging.handlers


def file_logger(log_path="runtime.log", log_level="DEBUG", log_format=None,
                time_rotating='D', encoding='utf-8', name=None):
    """
    创建一个文件日志记录器

    :param log_path: str, 日志文件路径，默认为"runtime.log"
    :param log_level: str, 日志级别，ERROR/WARNING/INFO/DEBUG， 默认为"DEBUG"
    :param log_format: str, 每条日志输出格式，默认为"[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d-%(module)s] %(message)s"
    :param time_rotating: str, 日志切割时间，默认为"D"，可选值: S(秒)/M(分)/H(小时)/D(天)/W(周)/midnight(深夜)
    :param encoding: str, 编码，默认为"utf-8"
    :param name: str, 日志记录器名称，默认为当前模块名

    :return: logger, 日志记录器对象
    """
    # 如果没有传入name参数，则使用当前模块名
    if not name:
        name = __name__
    # 创建一个日志记录器对象
    logger = logging.getLogger(name)
    # 设置日志记录器的日志级别
    logger.setLevel(log_level.upper())

    # 如果没有传入log_format参数，则使用默认的日志输出格式
    if log_format is None:
        log_format = '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d-%(module)s] %(message)s'
    # 创建一个日志输出格式对象
    formatter = logging.Formatter(log_format)

    # 如果传入了time_rotating参数，则创建一个按时间切割的日志文件处理器
    if time_rotating:
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_path, when=time_rotating, encoding=encoding)
    # 否则创建一个普通的日志文件处理器
    else:
        file_handler = logging.FileHandler(
            log_path, encoding=encoding)

    # 设置日志文件处理器的日志级别和输出格式
    file_handler.setLevel(level=log_level)
    file_handler.setFormatter(formatter)
    # 将日志文件处理器添加到日志记录器中
    logger.addHandler(file_handler)

    # 返回日志记录器对象
    return logger


if __name__ == "__main__":
    logger = file_logger()
    logger.info("info")
    logger.debug("debug")