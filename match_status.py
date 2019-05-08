import enum


class MatchStatus(enum.Enum):
    scheduled = '未开始'
    closed = '已结束'
    created = '已创建'
    inprogress = '进行中'

    @staticmethod
    def get_des(name):
        print(name)
        for n, des in MatchStatus.__members__.items():
            if des.name == name:
                return des.value
        return ''
