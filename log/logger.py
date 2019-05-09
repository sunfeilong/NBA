import logging
import logging.handlers

from project_config import ProjectConfig


class LoggerFactory:
    """
    日志类工厂，用于快速初始化日志类
    """

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s %(name)s thread:[%(thread)d - %(threadName)s] '
        '[%(module)s_%(funcName)s line: %(lineno)d] '
        'msg:[%(message)s]')

    info_file = ProjectConfig.get_log_dir() + 'info_nba_live.log'
    debug_file = ProjectConfig.get_log_dir() + 'debug_nba_live.log'

    info_handler = logging.handlers.RotatingFileHandler(
        filename=info_file, maxBytes=1024 * 1024 * 10, encoding='utf-8', backupCount=10)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    debug_handler = logging.handlers.RotatingFileHandler(
        filename=debug_file, maxBytes=1024 * 1024 * 10, encoding='utf-8', backupCount=10)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    common_log = logger = logging.getLogger('common log')
    common_log.setLevel(logging.DEBUG)
    common_log.addHandler(debug_handler)
    common_log.addHandler(info_handler)

    @staticmethod
    def get_logger(name: str = 'DefaultLogger'):
        """
        获取日志类
        :param name: 日志名字
        :return:
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(LoggerFactory.debug_handler)
        logger.addHandler(LoggerFactory.info_handler)
        return logger
