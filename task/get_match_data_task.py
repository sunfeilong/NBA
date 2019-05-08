import datetime
import threading
import time


class GetMatchDataTask(threading.Thread):
    def __init__(self, match_container, data_fetch):
        super().__init__()
        self.setDaemon(True)
        self.match_container = match_container
        self.data_fetch = data_fetch

    def run(self):
        match_list = self.data_fetch.get_match_list(datetime.datetime.fromtimestamp(time.time()))
        if not match_list:
            print('no game!')
        else:
            for match in match_list:
                self.match_container.add_match(match)
