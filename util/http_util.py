import logging
from urllib import request


class HttpRequestUtil:
    def __init__(self):
        self.logger = logging.getLogger('HttpRequestUtil')
        self.logger.setLevel('INFO')

    def get(self, address: str):
        try:
            response = request.urlopen(address)
            return response.read().decode('utf-8')
        except Exception as e:
            self.logger.error('connect to {} exception!, message:{}'.format(address, e))
        return ''
