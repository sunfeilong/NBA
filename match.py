import functools

from enums.match_status import MatchStatus
from log.logger import LoggerFactory
from util import char_util


@functools.total_ordering
class Message:
    def __init__(self, message_id, des, ctime, mtime):
        self.message_id = message_id
        self.des = des
        self.ctime = ctime
        self.mtime = mtime

    def __eq__(self, o: object) -> bool:
        return self.ctime == getattr(o, 'ctime')

    def __lt__(self, other):
        return self.ctime < other.ctime

    def __gt__(self, other):
        return self.ctime > other.ctime


class Match:
    """
    比赛，对应一场具体的比赛
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
        """
        向 message 列表中添加消息
        :param message_list: 要填加的消息列表
        :return: None
        """
        if not message_list:
            return
        message_list.sort()
        if self.message_list:
            ctime = 0
            for message in self.message_list:
                if message.message_id:
                    ctime = max(ctime, message.ctime)

            for message in message_list:
                if message.ctime and message.ctime > ctime:
                    self.message_list.append(message)
                    self.logger.debug('max ctime {}, message.ctime:{}, message_des:{}'
                                      .format(ctime, message.ctime, message.des))
        else:
            self.message_list.extend(message_list)
        self.logger.info('after add message message size {}'.format(len(self.message_list)))

    def update_score(self, home_team_score, visiting_team_score):
        """
        更新比赛的比分
        :param home_team_score: 主队分数
        :param visiting_team_score: 客队分数
        :return:
        """
        self.home_team_score = home_team_score
        self.visiting_team_score = visiting_team_score

    def get_score(self):
        """
        获取主队和客队比分
        :return: (主队分数，客队分数)
        """
        return self.home_team_score, self.visiting_team_score

    def get_ton_n_message(self, n: int):
        """
        获取最新的n个消息
        :param n: 消息个数
        :return:
        """
        return self.message_list[-n:]

    def has_closed(self):
        """
        比赛是否已经结束
        :return:
        """
        return self.status == MatchStatus.closed.name
