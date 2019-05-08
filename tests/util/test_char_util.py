from unittest import TestCase
from util import char_util


class TestCharUtil(TestCase):
    def test_add_pad(self):
        self.assertEqual(len(char_util.add_pad('123')), 6)
        self.assertEqual(len(char_util.add_pad('abc')), 6)
        self.assertEqual(len(char_util.add_pad('什么')), 2)
