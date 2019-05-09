from urllib import request

from log.logger import LoggerFactory


class HttpRequestUtil:
    """
    HTTP 请求工具类
    """

    def __init__(self):
        self.logger = LoggerFactory.get_logger('HttpRequestUtil')

    def get(self, address: str):
        """
        Get 请求
        :param address: 请求地址
        :return: 请求的响应字符串
        """
        try:
            response = request.urlopen(address)
            response_str = response.read().decode('utf-8')
            return response_str
        except Exception as e:
            self.logger.error('connect to {} exception, message:{}'.format(address, e))
        return ''
