import threading
import time
from date_fetch import DataFetch
from match_container import MatchContainer
from log.logger import LoggerFactory


class GetMatchMessageTask(threading.Thread):
    def __init__(self, delay, match_id, data_match: DataFetch, match_container: MatchContainer):
        super().__init__()
        self.logger = LoggerFactory.get_logger('GetMatchMessageTask')
        self.fetch_times = 0
        self.delay = delay
        self.match_id = match_id
        self.data_fetch = data_match
        self.match_container = match_container
        self.setDaemon(True)

    def run(self):
        while self.match_container.is_not_finished(self.match_id) or self.fetch_times < 2:
            self.fetch_times += 1
            message_list = self.data_fetch.get_message_list(self.match_id)
            self.match_container.add_message(self.match_id, message_list)
            self.logger.info('add message to {}, message size:{}'.format(self.match_id, len(message_list)))
            time.sleep(self.delay)
