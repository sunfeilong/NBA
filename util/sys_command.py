import os

from log.logger import LoggerFactory


class SysCommand:
    """
    执行系统命令行命令
    """

    @staticmethod
    def clear():
        """
        清空命令行
        :return: None
        """
        try:
            result = os.system('clear')
        except BaseException as e:
            LoggerFactory.common_log.log('run clear command exception, {}'.format(e))
