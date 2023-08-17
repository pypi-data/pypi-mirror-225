from hackle.internal.metrics.metrics import Metrics


class ApiCallMetrics:

    @staticmethod
    def record(operation, sample, is_success):
        """
        :param str operation:
        :param hackle.internal.metrics.timer.TimerSample sample:
        :param bool is_success:
        """
        tags = {
            "operation": operation,
            "success": "true" if is_success else "false"
        }
        timer = Metrics.timer("api.call", tags)
        sample.stop(timer)
