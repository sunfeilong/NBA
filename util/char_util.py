import re

pattern = '[0-9a-zA-Z]'


def add_pad(text: str):
    """
    由于汉字和数字字母在命令行所占的宽度不一样，
    因此对于字符串中包含数字和字母的的在字符串前面添加和数字字母个数相等的空格
    :param text:
    :return: 填充后的字符串
    """
    count = len(re.findall(pattern, text))
    return ' ' * count + text
