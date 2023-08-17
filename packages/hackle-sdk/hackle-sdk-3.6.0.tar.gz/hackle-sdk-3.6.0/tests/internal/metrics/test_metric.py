from unittest import TestCase

from hackle.internal.metrics.metric import MetricId, MetricType, Metric


class MetricTest(TestCase):

    def test_metric_eq(self):
        m_1 = MetricStub(MetricId("id_1", {}, MetricType.COUNTER))
        m_1_1 = MetricStub(MetricId("id_1", {}, MetricType.COUNTER))
        m_2 = MetricStub(MetricId("id_2", {}, MetricType.COUNTER))

        self.assertEqual(m_1, m_1)
        self.assertEqual(m_1, m_1_1)
        self.assertNotEqual(m_1, None)
        self.assertNotEqual(m_1, "hello")
        self.assertNotEqual(m_1, m_2)

    def test_metric_hash(self):
        id_ = MetricId("id_1", {}, MetricType.COUNTER)
        metric = MetricStub(id_)

        self.assertEqual(id_.__hash__(), metric.__hash__())

    def test_metric_id_eq(self):
        id_ = MetricId("counter", {}, MetricType.COUNTER)
        self.assertEqual(id_, id_)

        self.assertNotEqual(
            MetricId("counter", {}, MetricType.COUNTER),
            None
        )

        self.assertNotEqual(
            MetricId("counter", {}, MetricType.COUNTER),
            "hello"
        )

        self.assertNotEqual(
            MetricId("counter", {}, MetricType.COUNTER),
            MetricId("counter", {"tag": "42"}, MetricType.COUNTER),
        )

        self.assertNotEqual(
            MetricId("counter", {"tag": "41"}, MetricType.COUNTER),
            MetricId("counter", {"tag": "42"}, MetricType.COUNTER),
        )

        self.assertEqual(
            MetricId("counter", {"a": "b", "c": "d", "tag": "42"}, MetricType.COUNTER),
            MetricId("counter", {"tag": "42", "a": "b", "c": "d"}, MetricType.COUNTER),
        )

        self.assertEqual(
            MetricId("counter", {"tag": "42"}, MetricType.COUNTER),
            MetricId("counter", {"tag": "42"}, MetricType.TIMER),
        )


class MetricStub(Metric):

    def measure(self):
        return []
