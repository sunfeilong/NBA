import datetime
import logging.handlers
import os
import time

from date_fetch import SinaDataFetch
from match_container import MatchContainer
from match_status import MatchStatus
from task.get_match_data_task import GetMatchDataTask

my_logger = logging.getLogger("Logger")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.handlers.RotatingFileHandler(filename='log1.log', maxBytes=1024 * 10, backupCount=10)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
my_logger.addHandler(handler)

data_fetch = SinaDataFetch()
match_container = MatchContainer()
task_list = []
delay = 5


# 获取比赛列表
def fetch_match_list():
    match_list = data_fetch.get_match_list(datetime.datetime.fromtimestamp(time.time()))
    if not match_list:
        print('no game!')
    else:
        for match in match_list:
            match_container.add_match(match)


def fetch_message_list():
    for match in match_container.get_match_list():
        fetch_message_task = GetMatchDataTask(delay, match.match_id, data_fetch, match_container)
        fetch_message_task.setName('Get Message Task {} VS {}'.format(match.home_team, match.visiting_team))
        fetch_message_task.start()
        task_list.append(fetch_message_task)


if __name__ == "__main__":
    while True:
        try:
            fetch_match_list()
            fetch_message_list()
        except:
            print('系统异常')
            break

        index_id_dict = {}
        os.system('clear')
        try:
            # 输出比赛信息 选择比赛
            for index, match in enumerate(match_container.get_match_list()):
                index_id_dict[index] = match.match_id
                print('[ {:<2}]: {:<4} VS {:>4} {:>4} {:>5}'.format(index, match.home_team, match.visiting_team,
                                                                    MatchStatus.get_des(match.status),
                                                                    match.time))
            select = input('请选择一个比赛(输入 [q/Q] 退出): ')
            if select.lower() == 'q':
                break

            select = int(select)
            if not select in index_id_dict:
                continue

            match_container.update_select_match_id(index_id_dict[select])
            # 输出比赛信息
            while True:
                os.system('clear')
                message_list = match_container.get_data(index_id_dict[select], 10)
                for message in message_list:
                    print(message.des)
                time.sleep(delay)
        except BaseException as e:
            my_logger.error(e)
