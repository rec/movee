from ascript import util
from unittest import TestCase


class StableHashTest(TestCase):
    def test_simple(self):
        assert util.stable_hash('')[:16] == '69217a3079908094'
        assert util.stable_hash(' ')[:16] == 'e824451a0c7ba8bf'
        assert util.stable_hash('abc')[:16] == '508c5e8c327c14e2'
        assert util.stable_hash(b'abc')[:16] == '508c5e8c327c14e2'
