import configparser


class ProjectConfig:
    """
    项目配置信息，从配置文件中读取配置数据
    """

    config_parse = configparser.ConfigParser()
    config_parse.read('config.cfg')
    task_section = config_parse.sections()[0]
    match_section = config_parse.sections()[1]
    log_section = config_parse.sections()[2]

    @staticmethod
    def get_log_dir():
        """
        获取日志文件目录
        :return:  日志文件目录
        """
        return ProjectConfig.config_parse.get(ProjectConfig.log_section, 'logDir')

    @staticmethod
    def get_fetch_message_delay():
        """
        获取拉取数据延迟，单位：秒
        :return:  拉取数据的延迟
        """
        return ProjectConfig.config_parse.getint(ProjectConfig.task_section, 'delay')

    @staticmethod
    def get_show_message_size():
        """
        获取展示的比赛消息的数量
        :return:
        """
        return ProjectConfig.config_parse.getint(ProjectConfig.match_section, 'showMessageSize')
