import math
import os
import time
from configparser import ConfigParser

from date_fetch import SinaDataFetch
from log.logger import LoggerFactory
from match_container import MatchContainer
from match_status import MatchStatus
from task.get_match_data_task import GetMatchDataTask
from task.get_match_message_task import GetMatchMessageTask
from util.sys_command import SysCommand

my_logger = LoggerFactory.get_logger("start")


class NBALive:
    def __init__(self, config_file):
        self.logger = LoggerFactory.get_logger("RunNBALive")
        self.config = ConfigParser()
        self.config.read(config_file)
        task_s = self.config.sections()[0]
        match_s = self.config.sections()[1]
        self.delay = self.config.getint(task_s, 'delay')
        self.message_size = self.config.getint(match_s, 'messageSize')
        self.data_fetch = SinaDataFetch()
        self.index_match_dict = {}

        self.get_match_data_task = None
        self.match_container = MatchContainer()
        self.fetch_message_task = {}

        self.logger.info('task delay: {}s'.format(self.delay))
        self.logger.info('message size: {}'.format(self.message_size))

    def run_get_match_data_task(self):
        if self.get_match_data_task:
            return
        else:
            get_match_data_task = GetMatchDataTask(self.match_container, self.data_fetch)
            get_match_data_task.setName("get data task")
            get_match_data_task.start()
            # 等待拉取比赛列表任务完成
            while not self.match_container.get_match_list():
                continue

    def run_get_match_message_task(self):
        for match in self.match_container.get_match_list():
            if match.match_id in self.fetch_message_task:
                self.logger.info('get match data task is running, match id {}'.format(match.match_id))
                continue
            else:
                fetch_message_task = GetMatchMessageTask(self.delay, match.match_id, self.data_fetch,
                                                         self.match_container)
                fetch_message_task.setName('Get Message Task {}'.format(match.match_id))
                fetch_message_task.start()
                self.logger.info('add new get match data task {}'.format(match.match_id))
                self.fetch_message_task[match.match_id] = fetch_message_task

    def format_game_list_info(self):
        try:
            width = os.get_terminal_size().columns
        except:
            width = 100
        result = '-' * width
        index = 1
        for match in self.match_container.get_match_list():
            match_format = '\n[{:>2} ]: {:>5} {:<3}VS{:>3} 当前比分: {:<3}:{:>3} 比赛状态:[{:>4}] ' \
                .format(index,
                        match.time,
                        match.home_team,
                        match.visiting_team,
                        match.home_team_score,
                        match.visiting_team_score,
                        MatchStatus.get_des(match.status))
            self.index_match_dict[index] = match.match_id
            length = math.ceil(len(match_format) / width) * width
            result += match_format
            result += ' ' * (length - len(match_format) - 1)
            result += '\n'
            index += 1
        result += '-' * width
        result += '\n'
        return result

    def get_match_message_info(self, match_id):
        result = ''
        message_list = self.match_container.get_message(match_id, self.message_size)
        for message in message_list:
            result += '{}\n'.format(message.des)
        return result

    def select_index(self):
        try:
            print()
            select = input('请选择一场比赛(输入 [q/Q] 退出):\n ')
            if select.lower() == 'q':
                return 0
            if not select.isdigit():
                return -1
            select = int(select)
            if not select in self.index_match_dict:
                return -1
            return select
        except BaseException as e:
            self.logger.error(e)
        return -1

    def start(self):
        # 启动数据获取任务
        try:
            nba_live.run_get_match_data_task()
            nba_live.run_get_match_message_task()
        except BaseException as e1:
            self.logger.error(e1)
            return
        while True:
            try:
                SysCommand.clear()
                # 输出比赛信息 选择比赛
                print(self.format_game_list_info())
                index = self.select_index()
                while index < 0:
                    SysCommand.clear()
                    print(self.format_game_list_info())
                    index = self.select_index()
                if index == 0:
                    print('Bye Bye')
                    return
                while True:
                    SysCommand.clear()
                    message_info = self.get_match_message_info(self.index_match_dict[index])
                    print(message_info)
                    time.sleep(self.delay)
            except BaseException as e2:
                self.logger.error(e2)


if __name__ == "__main__":
    try:
        nba_live = NBALive('config.cfg')
        nba_live.start()
    except BaseException as e:
        print(e)
