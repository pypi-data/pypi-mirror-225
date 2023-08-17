import time
from unittest import TestCase

from hackle.internal.time.clock import SYSTEM_CLOCK, SystemClock, Clock


class SystemClockTest(TestCase):
    def test_global(self):
        self.assertIsInstance(SYSTEM_CLOCK, SystemClock)

    def test_current_millis(self):
        sut = SystemClock()

        s = sut.current_millis()
        time.sleep(0.1)
        e = sut.current_millis()

        self.assertTrue(95 < e - s < 105)


class FixedClock(Clock):

    def __init__(self, current_millis, tick):
        """
        :param int current_millis:
        """
        super(FixedClock, self).__init__()
        self.__current_millis = current_millis
        self.__tick = tick

    def current_millis(self):
        return self.__current_millis

    def tick(self):
        return self.__tick
