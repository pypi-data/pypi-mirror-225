from unittest import TestCase

from hackle.internal.metrics.cumulative.cumulative_metric_registry import CumulativeMetricRegistry
from hackle.internal.metrics.delegate.delegating_metric_registry import DelegatingMetricRegistry
from hackle.internal.time.time_unit import NANOSECONDS, MILLISECONDS


class DelegatingTimerTest(TestCase):

    def test_return_zero_if_timer_is_empty(self):
        timer = DelegatingMetricRegistry().timer("timer")
        self.assertEqual(0, timer.count())
        self.assertEqual(0, timer.total_time(NANOSECONDS))
        self.assertEqual(0, timer.max(NANOSECONDS))
        self.assertEqual(0, timer.mean(NANOSECONDS))

    def test_delegate_to_registered_timer(self):
        delegating = DelegatingMetricRegistry()
        cumulative1 = CumulativeMetricRegistry()
        cumulative2 = CumulativeMetricRegistry()
        delegating.add(cumulative1)
        delegating.add(cumulative2)

        timer = delegating.timer("timer")
        timer.record(42, NANOSECONDS)

        self.assertEqual(42.0, timer.total_time(NANOSECONDS))
        self.assertEqual(42.0, delegating.timer("timer").total_time(NANOSECONDS))
        self.assertEqual(42.0, cumulative1.timer("timer").total_time(NANOSECONDS))
        self.assertEqual(42.0, cumulative2.timer("timer").total_time(NANOSECONDS))

    def test_measure(self):
        delegating = DelegatingMetricRegistry()
        timer = delegating.timer("timer")
        measurements = timer.measure()

        self.assertEqual(4, len(measurements))
        self.assertEqual(0, measurements[0].value)
        self.assertEqual(0, measurements[1].value)
        self.assertEqual(0, measurements[2].value)
        self.assertEqual(0, measurements[3].value)

        timer.record(42, MILLISECONDS)
        self.assertEqual(0, measurements[0].value)
        self.assertEqual(0, measurements[1].value)
        self.assertEqual(0, measurements[2].value)
        self.assertEqual(0, measurements[3].value)

        delegating.add(CumulativeMetricRegistry())
        timer.record(42, MILLISECONDS)
        self.assertEqual(1, measurements[0].value)
        self.assertEqual(42.0, measurements[1].value)
        self.assertEqual(42.0, measurements[2].value)
        self.assertEqual(42.0, measurements[3].value)
