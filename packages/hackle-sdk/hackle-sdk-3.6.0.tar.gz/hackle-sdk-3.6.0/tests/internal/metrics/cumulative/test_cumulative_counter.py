from unittest import TestCase

from hackle.internal.metrics.cumulative.cumulative_metric_registry import CumulativeMetricRegistry
from tests.support import Jobs


class CumulativeCounterTest(TestCase):
    def test_concurrency_increment(self):
        counter = CumulativeMetricRegistry().counter("counter")

        def task():
            for _ in range(100_000):
                counter.increment()

        jobs = Jobs(8, task)
        jobs.start_and_wait()

        self.assertEqual(800_000, counter.count())

    def test_measure(self):
        counter = CumulativeMetricRegistry().counter("counter")
        measurements = counter.measure()

        self.assertEqual(1, len(measurements))
        self.assertEqual(0.0, measurements[0].value)

        counter.increment(42)
        self.assertEqual(42.0, measurements[0].value)
