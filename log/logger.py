import logging
import logging.handlers


class LoggerFactory:
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s %(name)s thread:[%(thread)d - %(threadName)s] [%(module)s_%(funcName)s line: %(lineno)d] msg:[%(message)s]')

    info_handler = logging.handlers.RotatingFileHandler(filename='info_nba_live.log', maxBytes=1024 * 10,
                                                        encoding='utf-8',
                                                        backupCount=10)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    debug_handler = logging.handlers.RotatingFileHandler(filename='debug_nba_live.log', maxBytes=1024 * 1024 * 10,
                                                         encoding='utf-8',
                                                         backupCount=10)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    @staticmethod
    def get_logger(name: str = 'DefaultLogger'):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(LoggerFactory.debug_handler)
        logger.addHandler(LoggerFactory.info_handler)
        return logger
