from hackle.internal.http.http_client import HttpClient
from hackle.internal.logger.log import Log
from hackle.internal.metrics.timer import TimerSample
from hackle.internal.monitoring.metrics.api_call_metrics import ApiCallMetrics
from hackle.internal.time.time_unit import SECONDS
from hackle.internal.workspace.workspace import Workspace


class WorkspaceFetcher(object):
    def __init__(self, sdk_base_url, http_client, polling_interval_seconds, scheduler):
        """
        :param str sdk_base_url:
        :param HttpClient http_client:
        :param float polling_interval_seconds:
        :param Scheduler scheduler:
        """
        self.__sdk_url = sdk_base_url + '/api/v2/workspaces'
        self.__http_client = http_client
        self.__polling_interval_seconds = polling_interval_seconds
        self.__scheduler = scheduler
        self.__polling_job = None

        self.__workspace = None

    def fetch(self):
        """
        :rtype: Workspace or None
        """
        return self.__workspace

    def start(self):
        if self.__polling_job is None:
            self.__poll()
            self.__polling_job = self.__scheduler.schedule_periodically(
                self.__polling_interval_seconds,
                self.__polling_interval_seconds,
                SECONDS,
                self.__poll
            )

    def stop(self):
        if self.__polling_job is not None:
            self.__polling_job.cancel()
        self.__scheduler.close()

    def __poll(self):
        sample = TimerSample.start()
        try:
            data = self.__http_client.get(self.__sdk_url)
            ApiCallMetrics.record("get.workspace", sample, True)
            if data is not None:
                self.__workspace = Workspace(data)
        except Exception as e:
            ApiCallMetrics.record("get.workspace", sample, False)
            Log.get().error('Failed to poll Workspace: {}'.format(str(e)))
