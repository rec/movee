from ascript.waiter import Waiter
from .travis import IS_TRAVIS
from unittest import TestCase
import time

DT = 0.05 * (5 if IS_TRAVIS else 1)


class TestWaiter(TestCase):
    def test_success(self):
        results = []
        w = Waiter(lambda: results.append(0), 2.5 * DT, DT)
        w.start()
        time.sleep(4 * DT)
        assert not w.thread.is_alive()
        assert results == [0]

    def test_failure(self):
        results = []
        w = Waiter(lambda: results.append(0), 3 * DT, DT)
        w.start()
        time.sleep(DT)
        w.stop()
        time.sleep(2 * DT)
        assert not w.thread.is_alive()
        assert results == []
