from unittest import TestCase

from hackle.internal.concurrent.schedule.thread_scheduler import ThreadScheduler
from hackle.internal.metrics.flush.flush_counter import FlushCounter
from hackle.internal.metrics.flush.flush_metric_registry import FlushMetricRegistry
from hackle.internal.metrics.flush.flush_timer import FlushTimer


class FlushMetricRegistryTest(TestCase):

    def test_counter(self):
        counter = FlushMetricRegistryStub(ThreadScheduler(), 10000).counter("counter")
        self.assertIsInstance(counter, FlushCounter)

    def test_timer(self):
        timer = FlushMetricRegistryStub(ThreadScheduler(), 10).timer("timer")
        self.assertIsInstance(timer, FlushTimer)

    def test_publish_flushed_metric(self):
        registry = FlushMetricRegistryStub(ThreadScheduler(), 100000)

        registry.counter("counter")
        registry.counter("counter", {"tag-1": "tag-2"})
        registry.timer("timer")

        registry.publish()
        self.assertEqual(3, len(registry.flushed_metrics))
        self.assertEqual(3, len(registry.metrics))

        registry.timer("timer", {"tag-1": "tag-1"})
        registry.publish()
        self.assertEqual(7, len(registry.flushed_metrics))


class FlushMetricRegistryStub(FlushMetricRegistry):

    def __init__(self, scheduler, push_interval_millis):
        super(FlushMetricRegistryStub, self).__init__(scheduler, push_interval_millis)
        self.flushed_metrics = []

    def flush_metric(self, metrics):
        self.flushed_metrics.extend(metrics)
