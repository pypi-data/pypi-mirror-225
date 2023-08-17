from unittest import mock
from unittest.mock import Mock

from tests import base
from hackle.internal.model.entities import Slot, Bucket
from hackle.internal.evaluation.bucket.bucketer import Bucketer


class BucketerTest(base.BaseTest):

    def setUp(self):
        self.sut = Bucketer()

    def test_버켓에서_계산된_슬롯번호로_슬롯을_가져온다(self):
        # given
        slot = Mock(spec=Slot)
        bucket = Mock(spec=Bucket)
        bucket.get_slot_or_none.return_value = slot
        bucket.seed = 123
        bucket.slot_size = 10000

        with mock.patch.object(self.sut, '_calculate_slot_number',
                               wraps=self.sut._calculate_slot_number) as _calculate_slot_number:
            _calculate_slot_number.return_value = 320

            # when
            actual = self.sut.bucketing(bucket, 'test_id')

            # then
            bucket.get_slot_or_none.assert_called_once_with(320)
            _calculate_slot_number.assert_called_once_with('test_id', 123, 10000)
            assert actual == slot
