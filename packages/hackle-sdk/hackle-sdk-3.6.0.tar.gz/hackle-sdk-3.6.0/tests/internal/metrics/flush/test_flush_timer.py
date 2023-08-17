from unittest import TestCase

from hackle.internal.concurrent.atomic.atomic_integer import AtomicInteger
from hackle.internal.metrics.flush.flush_timer import FlushTimer
from hackle.internal.metrics.metric import MetricId, MetricType
from hackle.internal.metrics.timer import Timer
from hackle.internal.time.time_unit import NANOSECONDS, MILLISECONDS
from tests.support import Jobs


class FlushTimerTest(TestCase):
    def test_concurrency(self):
        timer = self.__timer()

        timers = [[] for _ in range(8)]
        number = AtomicInteger(0)

        def task():
            n = number.get_and_add(1)
            flushed_timer = []

            for i in range(100_000):
                if i % 2 == 0:
                    timer.record(2, NANOSECONDS)
                else:
                    flushed_timer.append(timer.flush())
            timers[n] = flushed_timer

        jobs = Jobs(8, task)
        jobs.start_and_wait()

        count = sum(map(lambda t: t.count(), sum(timers, []))) + timer.flush().count()

        self.assertEqual(400_000, count)

    def test_record(self):
        timer = self.__timer()
        for i in range(100):
            timer.record((i + 1), MILLISECONDS)
        self.assertEqual(100, timer.count())
        self.assertEqual(5050, timer.total_time(MILLISECONDS))
        self.assertEqual(100, timer.max(MILLISECONDS))
        self.assertEqual(50.5, timer.mean(MILLISECONDS))

        flushed_timer = timer.flush()
        self.assertIsInstance(flushed_timer, Timer)

        self.assertEqual(100, flushed_timer.count())
        self.assertEqual(5050, flushed_timer.total_time(MILLISECONDS))
        self.assertEqual(100, flushed_timer.max(MILLISECONDS))
        self.assertEqual(50.5, flushed_timer.mean(MILLISECONDS))

        self.assertEqual(0, timer.count())
        self.assertEqual(0, timer.total_time(MILLISECONDS))
        self.assertEqual(0, timer.max(MILLISECONDS))
        self.assertEqual(0, timer.mean(MILLISECONDS))

    @staticmethod
    def __timer():
        return FlushTimer(MetricId("timer", {}, MetricType.TIMER))
