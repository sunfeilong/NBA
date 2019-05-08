from util import char_util
from log.logger import LoggerFactory


class Message:
    def __init__(self, message_id, des):
        self.message_id = message_id
        self.des = des


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
            message_id = 0
            for message in self.message_list:
                if message.message_id:
                    message_id = message.message_id

            for message in message_list:
                if message_id < message.message_id:
                    self.message_list.append(message)
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
