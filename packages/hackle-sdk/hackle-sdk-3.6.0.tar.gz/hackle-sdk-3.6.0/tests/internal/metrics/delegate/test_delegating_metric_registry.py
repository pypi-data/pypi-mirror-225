from unittest import TestCase

from hackle.internal.concurrent.atomic.atomic_integer import AtomicInteger
from hackle.internal.metrics.cumulative.cumulative_metric_registry import CumulativeMetricRegistry
from hackle.internal.metrics.delegate.delegating_counter import DelegatingCounter
from hackle.internal.metrics.delegate.delegating_metric_registry import DelegatingMetricRegistry
from hackle.internal.metrics.delegate.delegating_timer import DelegatingTimer
from hackle.internal.metrics.metric_registry import MetricRegistry
from tests.support import Jobs


class DelegatingMetricRegistryTest(TestCase):

    def test_counter(self):
        counter = DelegatingMetricRegistry().counter("counter")
        self.assertIsInstance(counter, DelegatingCounter)

    def test_timer(self):
        timer = DelegatingMetricRegistry().timer("timer")
        self.assertIsInstance(timer, DelegatingTimer)

    def test_DelegatingMetricRegistry_should_NOT_be_added(self):
        registry = DelegatingMetricRegistry()

        registry.add(DelegatingMetricRegistry())
        registry.add(DelegatingMetricRegistry())
        registry.add(DelegatingMetricRegistry())
        registry.add(DelegatingMetricRegistry())
        registry.add(DelegatingMetricRegistry())

        counter = registry.counter("counter")
        counter.increment()

        self.assertEqual(0, counter.count())

    def test_already_registered_registry_should_NOT_be_added(self):
        delegating = DelegatingMetricRegistry()
        cumulative = CumulativeMetricRegistry()

        delegating.add(cumulative)
        delegating.add(cumulative)
        delegating.add(cumulative)
        delegating.add(cumulative)

        counter = delegating.counter("counter")
        counter.increment()

        self.assertEqual(1, cumulative.counter("counter").count())

    def test_metric_before_registry_add(self):
        delegating = DelegatingMetricRegistry()
        delegating_counter = delegating.counter("counter")
        delegating_counter.increment()

        self.assertEqual(0, delegating_counter.count())

        cumulative = CumulativeMetricRegistry()
        delegating.add(cumulative)

        delegating_counter.increment()
        self.assertEqual(1, delegating_counter.count())
        self.assertEqual(1, cumulative.counter("counter").count())

    def test_concurrency(self):
        registry = DelegatingMetricRegistry()

        cumulative_registries = [CumulativeMetricRegistry() for _ in range(500)]
        task_number = AtomicInteger(-1)

        def task():
            n = task_number.add_and_get(1)
            for i in range(500):
                index = int(i / 2) + (250 * n)
                if i % 2 == 0:
                    registry.counter(index)
                else:
                    registry.add(cumulative_registries[index])

        jobs = Jobs(2, task)
        jobs.start_and_wait()
        self.assertEqual(500, len(registry.metrics))
        for i in range(500):
            name = str(i)
            registry.counter(name).increment()
            count = sum(map(lambda c: c.counter(name).count(), cumulative_registries))
            self.assertEqual(500, count)

    def test_close(self):
        class RegistryStub(MetricRegistry):
            def __init__(self):
                super(RegistryStub, self).__init__()
                self.is_closed = False

            def create_counter(self, id_):
                pass

            def create_timer(self, id_):
                pass

            def close(self):
                self.is_closed = True

        delegating = DelegatingMetricRegistry()
        registry_1 = RegistryStub()
        registry_2 = RegistryStub()

        delegating.add(registry_1)
        delegating.add(registry_2)

        delegating.close()

        self.assertTrue(registry_1.is_closed)
        self.assertTrue(registry_2.is_closed)
