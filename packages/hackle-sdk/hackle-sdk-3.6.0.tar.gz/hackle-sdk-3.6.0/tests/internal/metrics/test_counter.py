from unittest import TestCase

from hackle.internal.metrics.counter import CounterBuilder
from hackle.internal.metrics.cumulative.cumulative_metric_registry import CumulativeMetricRegistry
from hackle.internal.metrics.metric import MetricId, MetricType


class CounterTest(TestCase):
    def test_counter_builder(self):
        counter = CounterBuilder("test_counter") \
            .tags({"a": "1", "b": "2"}) \
            .tag("c", "3") \
            .register(CumulativeMetricRegistry())

        self.assertEqual(
            MetricId("test_counter", {"a": "1", "b": "2", "c": "3"}, MetricType.COUNTER),
            counter.id
        )
