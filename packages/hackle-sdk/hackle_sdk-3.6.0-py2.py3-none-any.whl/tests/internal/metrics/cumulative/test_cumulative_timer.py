from unittest import TestCase

from hackle.internal.metrics.cumulative.cumulative_metric_registry import CumulativeMetricRegistry
from hackle.internal.time.time_unit import NANOSECONDS, MILLISECONDS
from tests.support import Jobs


class CumulativeTimerTest(TestCase):
    def test_negative_duration_should_be_ignored(self):
        timer = CumulativeMetricRegistry().timer("timer")
        timer.record(-1, NANOSECONDS)
        self.assertEqual(0, timer.count())

    def test_concurrency_record(self):
        timer = CumulativeMetricRegistry().timer("timer")

        def task():
            for i in range(0, 100_000):
                timer.record(i + 1, NANOSECONDS)

        jobs = Jobs(8, task)
        jobs.start_and_wait()

        self.assertEqual(800_000.0, timer.count())
        self.assertEqual(40000400000.0, timer.total_time(NANOSECONDS))
        self.assertEqual(100_000.0, timer.max(NANOSECONDS))
        self.assertEqual(50_000.5, timer.mean(NANOSECONDS))

    def test_measure(self):
        timer = CumulativeMetricRegistry().timer("timer")
        measurements = timer.measure()

        self.assertEqual(4, len(measurements))
        self.assertEqual("count", measurements[0].name)
        self.assertEqual("total", measurements[1].name)
        self.assertEqual("max", measurements[2].name)
        self.assertEqual("mean", measurements[3].name)

        self.assertEqual(0.0, measurements[0].value)
        self.assertEqual(0.0, measurements[1].value)
        self.assertEqual(0.0, measurements[2].value)
        self.assertEqual(0.0, measurements[3].value)

        timer.record(42, MILLISECONDS)
        self.assertEqual(1.0, measurements[0].value)
        self.assertEqual(42.0, measurements[1].value)
        self.assertEqual(42.0, measurements[2].value)
        self.assertEqual(42.0, measurements[3].value)
