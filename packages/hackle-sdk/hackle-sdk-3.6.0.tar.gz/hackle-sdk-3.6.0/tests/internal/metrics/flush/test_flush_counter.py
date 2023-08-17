from unittest import TestCase

from hackle.internal.concurrent.atomic.atomic_integer import AtomicInteger
from hackle.internal.metrics.flush.flush_counter import FlushCounter
from hackle.internal.metrics.metric import MetricId, MetricType
from tests.support import Jobs


class FlushCounterTest(TestCase):
    def test_concurrency(self):
        counter = self.__counter()

        counters = [[] for _ in range(8)]
        number = AtomicInteger(0)

        def task():
            n = number.get_and_add(1)
            flushed_counter = []
            for i in range(100_000):
                if i % 2 == 0:
                    counter.increment(2)
                else:
                    flushed_counter.append(counter.flush())

            counters[n] = flushed_counter

        jobs = Jobs(8, task)
        jobs.start_and_wait()

        count = sum(map(lambda c: c.count(), sum(counters, []))) + counter.flush().count()
        self.assertEqual(800_000, count)

    def test_increment_with_flush(self):
        counter = self.__counter()

        counter.increment()
        self.assertEqual(1, counter.count())

        flushed_counter = counter.flush()
        self.assertEqual(0, counter.count())
        self.assertEqual(1, flushed_counter.count())

        counter.increment(42)
        self.assertEqual(42, counter.count())

    def test_measure(self):
        counter = self.__counter()
        counter.increment(42)
        measurements = counter.measure()

        self.assertEqual(42, measurements[0].value)

        counter.flush()
        self.assertEqual(0, measurements[0].value)

    def __counter(self):
        return FlushCounter(MetricId("counter", {}, MetricType.COUNTER))
