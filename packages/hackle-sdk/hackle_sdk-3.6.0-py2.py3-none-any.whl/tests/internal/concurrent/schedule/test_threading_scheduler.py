import time
from unittest import TestCase

from hackle.internal.concurrent.atomic.atomic_integer import AtomicInteger
from hackle.internal.concurrent.schedule.thread_scheduler import ThreadScheduler
from hackle.internal.time.time_unit import MILLISECONDS


class ThreadSchedulerTest(TestCase):
    def test_schedule(self):
        count = AtomicInteger()

        def task():
            count.add_and_get(1)

        scheduler = ThreadScheduler()
        job = scheduler.schedule_periodically(50, 100, MILLISECONDS, task)
        time.sleep(1)
        job.cancel()
        self.assertEqual(10, count.get())

    def test_ignore_exception(self):
        count = AtomicInteger()

        def task():
            count.add_and_get(1)
            raise Exception()

        scheduler = ThreadScheduler()
        job = scheduler.schedule_periodically(50, 100, MILLISECONDS, task)
        time.sleep(1)
        job.cancel()
        self.assertEqual(10, count.get())

    def test_cancel_during_delay(self):
        count = AtomicInteger()

        def task():
            count.add_and_get(1)

        scheduler = ThreadScheduler()
        job = scheduler.schedule_periodically(1000, 100, MILLISECONDS, task)
        time.sleep(0.5)
        job.cancel()
        self.assertEqual(0, count.get())

    def test_long_task(self):
        count = AtomicInteger()

        def long_task():
            time.sleep(0.4)
            count.add_and_get(1)

        scheduler = ThreadScheduler()
        job = scheduler.schedule_periodically(0, 100, MILLISECONDS, long_task)
        time.sleep(1)
        job.cancel()
        self.assertEqual(2, count.get())
