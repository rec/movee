from scripta.stable_hash import stable_hash
from unittest import TestCase


class StableHashTest(TestCase):
    def test_simple(self):
        assert stable_hash('')[:16] == '69217a3079908094'
        assert stable_hash(' ')[:16] == 'e824451a0c7ba8bf'
        assert stable_hash('abc')[:16] == '508c5e8c327c14e2'
        assert stable_hash(b'abc')[:16] == '508c5e8c327c14e2'
