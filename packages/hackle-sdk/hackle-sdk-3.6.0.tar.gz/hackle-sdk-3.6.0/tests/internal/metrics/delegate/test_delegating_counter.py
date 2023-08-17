from unittest import TestCase

from hackle.internal.metrics.cumulative.cumulative_metric_registry import CumulativeMetricRegistry
from hackle.internal.metrics.delegate.delegating_metric_registry import DelegatingMetricRegistry


class DelegatingCounterTest(TestCase):

    def test_return_zero_if_counter_is_empty(self):
        counter = DelegatingMetricRegistry().counter("counter")
        counter.increment()
        self.assertEqual(0, counter.count())

    def test_delegate_to_registered_counter(self):
        delegating = DelegatingMetricRegistry()
        cumulative1 = CumulativeMetricRegistry()
        cumulative2 = CumulativeMetricRegistry()

        delegating.add(cumulative1)
        delegating.add(cumulative2)

        delegating.counter("counter").increment(42)

        self.assertEqual(42, delegating.counter("counter").count())
        self.assertEqual(42, cumulative1.counter("counter").count())
        self.assertEqual(42, cumulative2.counter("counter").count())

    def test_measure(self):
        delegating = DelegatingMetricRegistry()
        counter = delegating.counter("counter")
        measurements = counter.measure()

        self.assertEqual(1, len(measurements))
        self.assertEqual(0, measurements[0].value)

        counter.increment(42)
        self.assertEqual(0, measurements[0].value)

        delegating.add(CumulativeMetricRegistry())
        counter.increment(42)
        self.assertEqual(42, measurements[0].value)
