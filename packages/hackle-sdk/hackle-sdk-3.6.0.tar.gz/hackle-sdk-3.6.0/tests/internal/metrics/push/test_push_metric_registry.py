from unittest import TestCase

from hackle.internal.concurrent.schedule.scheduler import Scheduler, ScheduledJob
from hackle.internal.metrics.noop.noop_counter import NoopCounter
from hackle.internal.metrics.noop.noop_timer import NoopTimer
from hackle.internal.metrics.push.push_metric_registry import PushMetricRegistry


class PushMetricRegistryTest(TestCase):

    def test_start_scheduling(self):
        scheduler = SchedulerStub()
        registry = PushMetricRegistryStub(scheduler, 42)

        registry.start()

        self.assertEqual(1, len(scheduler.jobs))

    def test_schedule_only_once(self):
        scheduler = SchedulerStub()
        registry = PushMetricRegistryStub(scheduler, 42)

        registry.start()
        registry.start()
        registry.start()
        registry.start()
        registry.start()

        self.assertEqual(1, len(scheduler.jobs))

    def test_stop_cancel_scheduling(self):
        scheduler = SchedulerStub()
        registry = PushMetricRegistryStub(scheduler, 42)

        registry.start()
        registry.stop()

        self.assertTrue(scheduler.jobs[0].is_canceled)

    def test_stop_should_be_publish(self):
        scheduler = SchedulerStub()
        registry = PushMetricRegistryStub(scheduler, 42)

        registry.start()
        registry.stop()

        self.assertEqual(1, registry.publish_count)

    def test_stop_not_started(self):
        scheduler = SchedulerStub()
        registry = PushMetricRegistryStub(scheduler, 42)

        registry.stop()
        self.assertEqual(0, registry.publish_count)

    def test_close(self):
        scheduler = SchedulerStub()
        registry = PushMetricRegistryStub(scheduler, 42)

        registry.start()
        registry.close()

        self.assertTrue(scheduler.jobs[0].is_canceled)
        self.assertTrue(scheduler.is_closed)


class PushMetricRegistryStub(PushMetricRegistry):

    def __init__(self, scheduler, push_interval_millis):
        super(PushMetricRegistryStub, self).__init__(scheduler, push_interval_millis)
        self.publish_count = 0

    def publish(self):
        self.publish_count += 1

    def create_counter(self, id_):
        return NoopCounter(id_)

    def create_timer(self, id_):
        return NoopTimer(id_)


class SchedulerStub(Scheduler):

    def __init__(self):
        super(SchedulerStub, self).__init__()
        self.jobs = []
        self.is_closed = False

    def schedule_periodically(self, delay, period, unit, task):
        job = self.Job()
        self.jobs.append(job)
        return job

    def close(self):
        self.is_closed = True

    class Job(ScheduledJob):

        def __init__(self):
            super().__init__()
            self.is_canceled = False

        def cancel(self):
            self.is_canceled = True
