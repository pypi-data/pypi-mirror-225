import time
from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.concurrent.schedule.scheduler import Scheduler, ScheduledJob
from hackle.internal.concurrent.schedule.thread_scheduler import ThreadScheduler
from hackle.internal.http.http_client import HttpClient
from hackle.internal.workspace.workspace_fetcher import WorkspaceFetcher


class WorkspaceFetcherTest(TestCase):

    def setUp(self):
        self.http_client = Mock(spec=HttpClient)
        self.http_client.get.return_value = '{}'

    def __workspace_fetcher(self, http_client=None, polling_interval_seconds=10.0, scheduler=ThreadScheduler()):
        return WorkspaceFetcher('localhost', http_client or self.http_client, polling_interval_seconds, scheduler)

    def test__fetch__without_start(self):
        sut = self.__workspace_fetcher()
        self.assertIsNone(sut.fetch())

    def test__start__poll(self):
        sut = self.__workspace_fetcher()

        sut.start()

        self.assertIsNotNone(sut.fetch())

    def test__start__once(self):
        scheduler = Mock(spec=Scheduler)
        scheduler.schedule_periodically.return_value = Mock()

        sut = self.__workspace_fetcher(scheduler=scheduler)

        for _ in range(0, 10):
            sut.start()

        scheduler.schedule_periodically.assert_called_once()

    def test__start__long_task_polling(self):
        http_client = DelayedHttpClient(0.25)
        sut = self.__workspace_fetcher(http_client=http_client, polling_interval_seconds=0.1)

        sut.start()
        time.sleep(0.4)

        self.assertEqual(3, http_client.call_count)  # 0, 250, 350 fetch / 100, 200 ignored

    def test__stop__cancel_polling_job(self):
        scheduler = Mock(spec=Scheduler)
        job = Mock(spec=ScheduledJob)
        scheduler.schedule_periodically.return_value = job

        sut = self.__workspace_fetcher(scheduler=scheduler)
        sut.start()
        sut.stop()

        job.cancel.assert_called_once()

    def test__stop__without_start(self):
        scheduler = Mock(spec=Scheduler)
        job = Mock(spec=ScheduledJob)
        scheduler.schedule_periodically.return_value = job

        sut = self.__workspace_fetcher(scheduler=scheduler)
        sut.stop()

        job.cancel.assert_not_called()


class DelayedHttpClient(object):

    def __init__(self, delay):
        self.__delay = delay
        self.__count = 0

    def get(self, url):
        self.__count += 1
        time.sleep(self.__delay)
        return '{}'

    @property
    def call_count(self):
        return self.__count
