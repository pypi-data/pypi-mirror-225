from unittest import TestCase

from hackle.internal.metrics.cumulative.cumulative_counter import CumulativeCounter
from hackle.internal.metrics.cumulative.cumulative_metric_registry import CumulativeMetricRegistry
from hackle.internal.metrics.delegate.delegating_metric import DelegatingMetric
from hackle.internal.metrics.metric import MetricId, MetricType
from hackle.internal.metrics.noop.noop_counter import NoopCounter
from tests.support import Jobs


class DelegatingMetricTest(TestCase):

    def test_add_concurrency(self):
        delegating_metric = DelegatingMetricStub(MetricId("test", {}, MetricType.COUNTER))

        def task():
            for i in range(10_000):
                if i % 2 == 0:
                    metrics = delegating_metric.metrics
                else:
                    delegating_metric.add(CumulativeMetricRegistry())

        jobs = Jobs(2, task)
        jobs.start_and_wait()
        self.assertEqual(10_000, len(delegating_metric.metrics))

    def test_if_metric_is_not_registered_noop_metric_should_be_returned(self):
        delegating_metric = DelegatingMetricStub(MetricId("test", {}, MetricType.COUNTER))
        self.assertIsInstance(delegating_metric.first(), NoopCounter)

    def test_return_registered_metric(self):
        delegating_metric = DelegatingMetricStub(MetricId("test", {}, MetricType.COUNTER))
        delegating_metric.add(CumulativeMetricRegistry())
        self.assertIsInstance(delegating_metric.first(), CumulativeCounter)


class DelegatingMetricStub(DelegatingMetric):

    def __init__(self, id_):
        super(DelegatingMetricStub, self).__init__(id_)

    def noop_metric(self):
        return NoopCounter(self.id)

    def register_metric(self, registry):
        return registry.create_counter(self.id)

    def measure(self):
        pass
