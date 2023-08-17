from unittest import TestCase

from hackle.internal.metrics.measurement import Measurement, Measurements


class MeasurementTest(TestCase):
    def test_measurement_value(self):
        it = [1, 2, 3, 4].__iter__()
        measurement = Measurement("count", lambda: it.__next__())

        self.assertEqual(1.0, measurement.value)
        self.assertEqual(2.0, measurement.value)

    def test_measurement_name(self):
        self.assertEqual("count", Measurements.COUNT)
        self.assertEqual("total", Measurements.TOTAL)
        self.assertEqual("max", Measurements.MAX)
        self.assertEqual("mean", Measurements.MEAN)
