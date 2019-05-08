from util import char_util
from log.logger import LoggerFactory


class Message:
    def __init__(self, message_id, des, ctime, mtime):
        self.message_id = message_id
        self.des = des
        self.ctime = ctime
        self.mtime = mtime


class Match:
    """
    比赛
    """

    def __init__(self, match_id, date, time, status, home_team, visiting_team, home_team_score, visiting_team_score):
        self.logger = LoggerFactory.get_logger('Match')
        self.match_id = match_id
        self.date = date
        self.time = time
        self.status = status
        self.home_team = char_util.add_pad(home_team)
        self.visiting_team = char_util.add_pad(visiting_team)
        self.home_team_score = home_team_score
        self.visiting_team_score = visiting_team_score
        self.message_list = []

    def add_message(self, message_list: list):
        if not message_list:
            return
        if self.message_list:
            ctime = 0
            for message in self.message_list:
                if message.message_id:
                    ctime = max(ctime, message.ctime)

            for message in message_list:
                if message.ctime and message.ctime > ctime:
                    self.message_list.append(message)
                    self.logger.info(
                        'message_id {}, message.message_id:{}, message_des:{}'.format(ctime, message.ctime,
                                                                                      message.des))
        else:
            self.message_list.extend(message_list)
        self.logger.info('after add message message size {}'.format(len(self.message_list)))

    def update_score(self, home_team_score, visiting_team_score):
        self.home_team_score = home_team_score
        self.visiting_team_score = visiting_team_score

    def get_score(self):
        return self.home_team_score, self.visiting_team_score

    def get_ton_n_message(self, n: int):
        return self.message_list[-n:]
