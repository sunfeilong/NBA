import re

pattern = '[0-9a-zA-Z]'


def add_pad(text: str):
    """
    数字和字母增加一个空格填充
    :param text:
    :return: 填充后的字符串
    """
    count = len(re.findall(pattern, text))
    return ' ' * count + text
