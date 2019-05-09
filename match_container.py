from match import Match
from match_status import MatchStatus


class MatchContainer:
    """
    Game 容存储存在的Game
    """

    def __init__(self):
        self.select_match_id = ''
        self.match = {}

    def add_or_update_match(self, match: Match):
        if match.match_id in self.match:
            self.match[match.match_id].home_team_score = match.home_team_score
            self.match[match.match_id].visiting_team_score = match.visiting_team_score
            self.match[match.match_id].status = match.status
        else:
            self.match[match.match_id] = match

    def add_message(self, match_id, data_list):
        self.__match(match_id).add_message(data_list)

    def get_message(self, match_id, top_n):
        return self.__match(match_id).get_ton_n_message(top_n)

    def update_score(self, match_id, home_team_score, visiting_team_score):
        self.__match(match_id).update_score(home_team_score, visiting_team_score)

    def update_select_match_id(self, select_match_id):
        self.select_match_id = select_match_id

    def is_not_finished(self, match_id):
        return not self.__match(match_id).status == MatchStatus.closed.name

    def __match(self, match_id) -> Match:
        if not match_id in self.match:
            raise Exception('参数非法:{}'.format(match_id))
        return self.match[match_id]

    def get_match_list(self):
        return self.match.values()

    def all_match_has_end(self):
        if not self.match:
            return True

        for match in self.match.values():
            if not match.has_closed():
                return False
        return True
