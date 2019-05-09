from unittest import TestCase
from date_fetch import SinaDataFetch

import time
import datetime


class TestSinaDatFetch(TestCase):
    def setUp(self):
        self.sina_data_fetch = SinaDataFetch()

    def test_get_game_list(self):
        result = self.sina_data_fetch.fetch_match_list(datetime.datetime.fromtimestamp(time.time()))
        self.assertIsNotNone(result)

    def test_get_data_list(self):
        result = self.sina_data_fetch.fetch_message_list('feb4ae76-49b1-43be-9cde-a2160e1769e4')
        self.assertIsNotNone(result)
        result = self.sina_data_fetch.fetch_message_list('1083c1c5-ddf8-460f-bccf-dc17d509d108')
        self.assertIsNotNone(result)
