import json
import datetime
import time

from match import Match
from match import Message
from util.http_util import HttpRequestUtil
from log.logger import LoggerFactory


class DataFetch:
    def get_match_list(self, date: str) -> list:
        """
        获取比赛列表
        :return:
        """
        pass

    def parse_message_list(self, match_id) -> list:
        """
        获取比赛数据
        :return:
        """
        pass


class SinaDataFetch(DataFetch):
    def __init__(self):
        self.http = HttpRequestUtil()
        self.logger = LoggerFactory.get_logger('SinaDataFetch')
        self.game_list_address = 'https://slamdunk.sports.sina.com.cn/api?p=radar&s=schedule&a=day&date={}&callback=dayCallback'
        self.data_live_address = 'https://slamdunk.sports.sina.com.cn/api?p=radar&s=boxscore&a=match&callback=cb_matchInfo_f23b83f6_2343_4ee2_8419_8ed143d954c1&mid={}&dpc=1'
        self.data_sport_address = 'http://rapid.sports.sina.com.cn/live/api/live/room?callback=cb_f23b83f6_2343_4ee2_8419_8ed143d954c1&match_id={}&dpc=1'
        self.data_list_address = 'http://rapid.sports.sina.com.cn/live/api/msg/index?callback=cb_livercast_f23b83f6_2343_4ee2_8419_8ed143d954c1&room_id={}&count=30&msg_id=''&direct=-1&dpc=1'

    def get_match_list(self, date) -> list:
        response = self.http.get(self.game_list_address.format(date))
        return self.parse_game_list(response)

    def parse_message_list(self, match_id) -> list:
        live_response = self.http.get(self.data_live_address.format(match_id))
        live_id = self.get_live_id(live_response)
        sport_response = self.http.get(self.data_sport_address.format(live_id))
        sport_id = self.get_sport_id(sport_response)
        data_response = self.http.get(self.data_list_address.format(sport_id))
        data_list = self.get_message_list(data_response)
        return data_list

    def parse_game_list(self, game_list_response):
        result = []
        start = game_list_response.index('(') + 1
        end = game_list_response.index(')')
        json_data = json.loads(game_list_response[start:end])
        match_list = json_data['result']['data']['matchs']
        for match in match_list:
            game = Match(match['mid'], match['date'], match['time'], match['status'], match['home']['name'],
                         match['away']['name'], match['home']['score'], match['away']['score'])
            result.append(game)
        return result

    def get_live_id(self, live_response):
        start = live_response.index('(') + 1
        end = live_response.index(')')
        json_data = json.loads(live_response[start:end])
        return json_data['result']['data']['livecast_id']

    def get_sport_id(self, sport_response):
        start = sport_response.index('(') + 1
        end = sport_response.index(')')
        json_data = json.loads(sport_response[start:end])
        return json_data['result']['data']['room_id']

    def get_message_list(self, data_list_response) -> list:
        result = []
        start = data_list_response.index('(') + 1
        end = data_list_response.index(')')
        json_data = json.loads(data_list_response[start:end])
        data_list = json_data['result']['data']
        for data in data_list:
            try:
                if not data['match']['phase']:
                    des = '[                           ] {:>2}: {:}'.format(data['liver']['nickname'], data['text'])
                else:
                    time_localtime = time.localtime(int(data['ctime']))
                    curr_time = '{}:{}'.format(time_localtime.tm_hour, time_localtime.tm_min)
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
                pass
        return result
