from unittest import TestCase

from hackle.internal.metrics.metric import MetricId, MetricType
from hackle.internal.metrics.noop.noop_timer import NoopTimer
from hackle.internal.time.time_unit import MILLISECONDS, NANOSECONDS


class NoopTimerTest(TestCase):
    def test_count_should_be_zero_even_if_recorded(self):
        timer = NoopTimer(MetricId("timer", {}, MetricType.COUNTER))
        self.assertEqual(0, timer.count())
        timer.record(42, MILLISECONDS)
        self.assertEqual(0, timer.count())
        self.assertEqual(0, timer.total_time(NANOSECONDS))
