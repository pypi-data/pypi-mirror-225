from unittest import TestCase

from hackle.internal.metrics.delegate.delegating_counter import DelegatingCounter
from hackle.internal.metrics.delegate.delegating_timer import DelegatingTimer
from hackle.internal.metrics.metrics import Metrics


class MetricsTest(TestCase):

    def test_metric(self):
        counter = Metrics.counter("counter")
        timer = Metrics.timer("timer")

        self.assertIsInstance(counter, DelegatingCounter)
        self.assertIsInstance(timer, DelegatingTimer)
