from unittest import TestCase

from hackle.internal.metrics.metric import MetricId, MetricType
from hackle.internal.metrics.noop.noop_counter import NoopCounter


class NoopCounterTest(TestCase):
    def test_count_should_be_zero_even_if_incremented(self):
        counter = NoopCounter(MetricId("counter", {}, MetricType.COUNTER))
        self.assertEqual(0, counter.count())
        counter.increment()
        self.assertEqual(0, counter.count())
