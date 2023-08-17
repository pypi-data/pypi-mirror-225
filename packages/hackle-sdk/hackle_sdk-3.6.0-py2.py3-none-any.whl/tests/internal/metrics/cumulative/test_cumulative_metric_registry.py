from unittest import TestCase

from hackle.internal.metrics.cumulative.cumulative_counter import CumulativeCounter
from hackle.internal.metrics.cumulative.cumulative_metric_registry import CumulativeMetricRegistry
from hackle.internal.metrics.cumulative.cumulative_timer import CumulativeTimer


class CumulativeMetricRegistryTest(TestCase):
    def test_counter(self):
        counter = CumulativeMetricRegistry().counter("counter")
        self.assertIsInstance(counter, CumulativeCounter)

    def test_timer(self):
        timer = CumulativeMetricRegistry().timer("timer")
        self.assertIsInstance(timer, CumulativeTimer)
