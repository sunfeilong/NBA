import datetime
import json

from log.logger import LoggerFactory
from match import Match
from match import Message
from util.http_util import HttpRequestUtil


class DataFetch:
    """
    数据抓取工具
    """

    def fetch_match_list(self, date: str) -> list:
        """
        获取比赛列表
        :return:
        """
        pass

    def fetch_message_list(self, match_id) -> list:
        """
        获取比赛数据
        :return:
        """
        pass


class SinaDataFetch(DataFetch):
    def __init__(self):
        self.http = HttpRequestUtil()
        self.logger = LoggerFactory.get_logger('SinaDataFetch')
        self.match_list_address = 'https://slamdunk.sports.sina.com.cn/api?p=radar&s=schedule&a=day&date={}&callback=dayCallback'
        self.data_live_address = 'https://slamdunk.sports.sina.com.cn/api?p=radar&s=boxscore&a=match&callback=cb_matchInfo_f23b83f6_2343_4ee2_8419_8ed143d954c1&mid={}&dpc=1'
        self.data_sport_address = 'http://rapid.sports.sina.com.cn/live/api/live/room?callback=cb_f23b83f6_2343_4ee2_8419_8ed143d954c1&match_id={}&dpc=1'
        self.data_list_address = 'http://rapid.sports.sina.com.cn/live/api/msg/index?callback=cb_livercast_f23b83f6_2343_4ee2_8419_8ed143d954c1&room_id={}&count=30&msg_id=''&direct=-1&dpc=1'

    def fetch_match_list(self, date) -> list:
        try:
            response = self.http.get(self.match_list_address.format(date))
            game_list = self._parse_match_list(response)

            # log
            match_info = []
            for match in game_list:
                match_info.append((match.match_id, match.home_team))
            self.logger.info('fetch_match_list, match info:{} '.format(match_info))

            return game_list
        except BaseException as e:
            self.logger.error('fetch_match_list exception {}'.format(e))

    def fetch_message_list(self, match_id) -> list:
        try:
            live_response = self.http.get(self.data_live_address.format(match_id))
            live_id = self._get_live_id(live_response)
            sport_response = self.http.get(self.data_sport_address.format(live_id))
            sport_id = self._get_sport_id(sport_response)
            message_response = self.http.get(self.data_list_address.format(sport_id))
            message_list = self._get_message_list(message_response)
            self.logger.info('fetch_message_list, match id: {} , message length: {} '.format(match_id, len(message_list)))
            return message_list
        except BaseException as e:
            self.logger.error('fetch_message_list exception {}'.format(e))
        return []

    def _parse_match_list(self, game_list_response):
        result = []
        try:
            json_data = json.loads(self._get_json_text_from(game_list_response))
            match_list = json_data['result']['data']['matchs']
            for match in match_list:
                game = Match(match['mid'], match['date'], match['time'], match['status'], match['home']['name'],
                             match['away']['name'], match['home']['score'], match['away']['score'])
                result.append(game)
        except BaseException as e:
            self.logger.error('parse_game_list exception {}'.format(e))
        return result

    def _get_live_id(self, live_response):
        try:
            json_data = json.loads(self._get_json_text_from(live_response))
            return json_data['result']['data']['livecast_id']
        except BaseException as e:
            self.logger.error('get_live_id exception {}'.format(e))
        return ''

    def _get_sport_id(self, sport_response):
        try:
            json_data = json.loads(self._get_json_text_from(sport_response))
            return json_data['result']['data']['room_id']
        except BaseException as e:
            self.logger.error('get_sport_id exception {}'.format(e))
        return ''

    def _get_message_list(self, data_list_response) -> list:
        result = []
        try:
            json_data = json.loads(self._get_json_text_from(data_list_response))
            data_list = json_data['result']['data']
            # 为什么把 des 封装到一个字符串里面，考虑到不同平台的数据不一样
            # 如果把信息存入 Message 的变量里面 后期组合比较麻烦
            # 所以就在这进行封装
            for data in data_list:
                try:
                    if not data['match']['phase']:
                        des = '[*******************************] {:>2}: {:}'.format(data['liver']['nickname'],
                                                                                   data['text'])
                    else:
                        curr_time = '{:%H:%M:%S}'.format(datetime.datetime.fromtimestamp(int(data['ctime'])))
                        des = '[{:>5}][{} 比分:({:<3}:{:>3})] {:>2}: {:}'.format(
                            curr_time,
                            data['match']['phase'],
                            data['match']['score1'],
                            data['match']['score2'],
                            data['liver']['nickname'],
                            data['text'])
                    message = Message(data['id'], des, int(data['ctime']), int(data['mtime']))
                    result.append(message)
                except BaseException as e:
                    self.logger.error('get message list {}'.format(e))
        except BaseException as e:
            self.logger.error('get message list {}'.format(e))
        return result

    @staticmethod
    def _get_json_text_from(response):
        start = response.index('(') + 1
        end = response.index(')')
        return response[start:end]
