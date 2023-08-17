from unittest import TestCase

from hackle.internal.metrics.cumulative.cumulative_metric_registry import CumulativeMetricRegistry
from hackle.internal.metrics.metric import MetricId, MetricType
from hackle.internal.metrics.timer import TimerBuilder


class TimerTest(TestCase):

    def test_timer_builder(self):
        timer = TimerBuilder("test_timer") \
            .tags({"a": "1", "b": "2"}) \
            .tag("c", "3") \
            .register(CumulativeMetricRegistry())

        self.assertEqual(
            MetricId("test_timer", {"a": "1", "b": "2", "c": "3"}, MetricType.TIMER),
            timer.id
        )
