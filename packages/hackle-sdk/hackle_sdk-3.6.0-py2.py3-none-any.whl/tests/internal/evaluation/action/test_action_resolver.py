import unittest
from unittest.mock import Mock

from hackle.internal.evaluation.action.action_resolver import ActionResolver
from hackle.internal.evaluation.bucket.bucketer import Bucketer
from hackle.internal.model.entities import TargetAction, Variation, Experiment, Bucket, Slot
from hackle.internal.user.internal_hackle_user import InternalHackleUser
from hackle.internal.workspace.workspace import Workspace
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request
from tests.internal.model.test_entities import create_experiment


class ActionResolverTest(unittest.TestCase):

    def setUp(self):
        self.bucketer = Mock(spec=Bucketer)
        self.sut = ActionResolver(self.bucketer)

    def test__unsupported_type(self):
        action = TargetAction(type='__INVALID__')

        actual = self.sut.resolve_or_none(create_experiment_request(), action)

        self.assertIsNone(actual)

    def test__variation_action__variation_id_에_해당하는_variation_을_가져온다(self):
        # given
        action = TargetAction(type='VARIATION', variation_id=420, bucket_id=None)
        variation = Mock(spec=Variation)
        experiment = Mock(spec=Experiment)
        experiment.id = 42
        experiment.get_variation_by_id_or_none.return_value = variation

        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.resolve_or_none(request, action)

        # then
        self.assertIsNotNone(actual)
        self.assertEqual(variation, actual)

    def test__variation_action__variation_id에_해당하는_Variation이_없으면_예외발생(self):
        # given
        action = TargetAction(type='VARIATION', variation_id=420)
        experiment = Mock(spec=Experiment)
        experiment.id = 42
        experiment.get_variation_by_id_or_none.return_value = None

        request = create_experiment_request(experiment=experiment)

        # when
        self.assertRaises(Exception, self.sut.resolve_or_none, request, action)

    def test__bucket_action__bucket_id에_해당하는_Bucket이_없으면_예외발생(self):
        # given
        action = TargetAction(type='BUCKET', bucket_id=320)
        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = None

        request = create_experiment_request(workspace=workspace)

        # when
        self.assertRaises(Exception, self.sut.resolve_or_none, request, action)

    def test__bucket_action__identifier_type에_해당하는_식별자가_없으면_None_리턴(self):
        # given
        user = InternalHackleUser(identifiers={'$id': 'test'}, properties={})
        action = TargetAction(type='BUCKET', bucket_id=320)
        bucket = Mock(spec=Bucket)
        experiment = create_experiment(identifier_type="custom_id")
        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = bucket

        request = create_experiment_request(workspace, user, experiment)

        # when
        actual = self.sut.resolve_or_none(request, action)

        # then
        self.assertIsNone(actual)

    def test__bucket_action__슬롯에_할당_안된경우_None(self):
        # given
        user = InternalHackleUser(identifiers={'$id': 'test'}, properties={})
        action = TargetAction(type='BUCKET', bucket_id=320)
        bucket = Mock(spec=Bucket)
        experiment = create_experiment()
        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = bucket
        self.bucketer.bucketing.return_value = None

        request = create_experiment_request(workspace, user, experiment)

        # when
        actual = self.sut.resolve_or_none(request, action)

        # then
        self.assertIsNone(actual)
        self.bucketer.bucketing.assert_called_once_with(bucket, 'test')

    def test__bucket_action__슬롯에_할당되었지만_슬롯의_variation_id에_해당하는_Variation이_없으면_None리턴(self):
        # given
        user = InternalHackleUser(identifiers={'$id': 'test'}, properties={})
        action = TargetAction(type='BUCKET', bucket_id=320)
        bucket = Mock(spec=Bucket)
        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = bucket

        slot = Slot(0, 100, 520)
        self.bucketer.bucketing.return_value = slot

        experiment = Mock(spec=Experiment)
        experiment.id = 42
        experiment.identifier_type = '$id'
        experiment.get_variation_by_id_or_none.return_value = None

        request = create_experiment_request(workspace, user, experiment)

        # when
        actual = self.sut.resolve_or_none(request, action)

        # then
        self.assertIsNone(actual)
        self.bucketer.bucketing.assert_called_once_with(bucket, 'test')
        experiment.get_variation_by_id_or_none.assert_called_once_with(520)

    def test__bucket_action__버켓팅을_통해_할당된_Variation을_리턴한다(self):
        # given
        user = InternalHackleUser(identifiers={'$id': 'test'}, properties={})
        action = TargetAction(type='BUCKET', bucket_id=320)
        bucket = Mock(spec=Bucket)
        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = bucket

        slot = Slot(0, 100, 520)
        self.bucketer.bucketing.return_value = slot

        experiment = Mock(spec=Experiment)
        experiment.id = 42
        experiment.identifier_type = '$id'
        experiment.get_variation_by_id_or_none.return_value = Variation(42, 'E', False)

        request = create_experiment_request(workspace, user, experiment)

        # when
        actual = self.sut.resolve_or_none(request, action)

        # then
        self.assertEqual(Variation(42, 'E', False), actual)
        self.bucketer.bucketing.assert_called_once_with(bucket, 'test')
        experiment.get_variation_by_id_or_none.assert_called_once_with(520)
