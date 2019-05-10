import datetime
import threading
import time
from log.logger import LoggerFactory


class GetMatchDataTask(threading.Thread):
    """
    拉取获取比赛信息的任务
    """

    def __init__(self, delay, match_container, data_fetch):
        super().__init__()
        self.logger = LoggerFactory.get_logger('GetMatchDataTask')
        self.setDaemon(True)
        self.fetch_times = 0
        self.delay = delay
        self.match_container = match_container
        self.data_fetch = data_fetch

    def run(self):
        while not self.match_container.all_match_has_end() or self.fetch_times < 2:
            try:
                self.fetch_times += 1
                match_list = self.data_fetch.fetch_match_list(datetime.datetime.fromtimestamp(time.time()))
                if not match_list:
                    print('no game!')
                else:
                    for match in match_list:
                        self.match_container.add_or_update_match(match)
            except BaseException as e:
                self.logger.error('GetMatchDataTask run exception: {}'.format(e))
            finally:
                time.sleep(max(5, self.delay))

        self.logger.info('GetMatchDataTask has end, fetch times: [{}] task name: {}'
                         .format(self.fetch_times, threading.current_thread().name))
