import time
from unittest import TestCase
from unittest.mock import Mock

from six.moves.queue import Queue

from hackle.internal.concurrent.schedule.thread_scheduler import ThreadScheduler
from hackle.internal.event.event_dispatcher import EventDispatcher
from hackle.internal.event.event_processor import EventProcessor
from hackle.internal.event.user_event import UserEvent
from tests.internal.concurrent.test_concurrent_supports import Jobs


class EventProcessorTest(TestCase):

    def setUp(self):
        self.event_dispatcher = Mock(spec=EventDispatcher)
        self.flush_scheduler = ThreadScheduler()
        self.queue = Queue(maxsize=1000)

    def __event_processor(
            self,
            queue=None,
            event_dispatcher=None,
            event_dispatch_size=100,
            flush_scheduler=ThreadScheduler(),
            flush_interval_seconds=10.0,
            shutdown_timeout_seconds=10.0):
        return EventProcessor(
            queue or self.queue,
            event_dispatcher or self.event_dispatcher,
            event_dispatch_size,
            flush_scheduler,
            flush_interval_seconds,
            shutdown_timeout_seconds
        )

    def test__process__invalid_event(self):
        sut = self.__event_processor()
        sut.process('test')

        self.assertEqual(0, self.queue.qsize())

    def test__process__not_dispatched_if_batch_size_is_not_reached(self):
        sut = self.__event_processor(event_dispatch_size=2, flush_interval_seconds=10)
        sut.start()

        sut.process(Mock(spec=UserEvent))
        time.sleep(1)

        self.event_dispatcher.dispatch.assert_not_called()

    def test__process__dispatch_when_batch_size_is_reached(self):
        sut = self.__event_processor(event_dispatch_size=2, flush_interval_seconds=10)

        sut.start()

        event = Mock(spec=UserEvent)
        sut.process(event)
        time.sleep(0.1)

        self.event_dispatcher.dispatch.assert_not_called()

        sut.process(event)
        time.sleep(0.1)

        self.event_dispatcher.dispatch.assert_called_once()

        sut.stop()

    def test__process__dispatch_when_interval_is_reached(self):
        sut = self.__event_processor(event_dispatch_size=1000, flush_interval_seconds=0.5)
        sut.start()

        sut.process(Mock(spec=UserEvent))
        sut.process(Mock(spec=UserEvent))
        sut.process(Mock(spec=UserEvent))
        sut.process(Mock(spec=UserEvent))
        sut.process(Mock(spec=UserEvent))
        time.sleep(0.7)

        self.event_dispatcher.dispatch.assert_called_once()

    def test__process__not_dispatch_if_events_is_empty(self):
        sut = self.__event_processor(event_dispatch_size=1000, flush_interval_seconds=0.1)
        sut.start()

        time.sleep(1)

        self.event_dispatcher.dispatch.assert_not_called()

    def test__process__ignore_when_queue_is_full(self):
        q = Queue(maxsize=1)
        sut = self.__event_processor(queue=q, event_dispatch_size=1000, flush_interval_seconds=0.1)

        for _ in range(0, 10):
            sut.process(Mock(spec=UserEvent))

        self.assertEqual(1, q.qsize())

    def test__process__concurrency(self):

        sut = self.__event_processor(queue=Queue(maxsize=16 * 10_000),
                                     event_dispatch_size=10,
                                     flush_interval_seconds=0.01)
        event = Mock(spec=UserEvent)

        def task():
            for i in range(10_000):
                sut.process(event)

        jobs = Jobs(16, task)

        sut.start()
        jobs.start_and_wait()

        sut.stop()

        count = sum(map(lambda it: len(it[0][0]), self.event_dispatcher.dispatch.call_args_list))
        self.assertEqual(16 * 10_000, count)
