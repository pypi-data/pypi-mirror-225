import unittest
from unittest.mock import Mock

from hackle.internal.evaluation.bucket.bucketer import Bucketer
from hackle.internal.evaluation.container.container_resolver import ContainerResolver
from hackle.internal.model.entities import Container, Bucket, Slot, ContainerGroup
from hackle.internal.user.internal_hackle_user import InternalHackleUser
from hackle.internal.workspace.workspace import Workspace
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request
from tests.internal.model.test_entities import create_experiment


class ContainerResolverTest(unittest.TestCase):

    def setUp(self):
        self.bucketer = Mock(spec=Bucketer)
        self.sut = ContainerResolver(self.bucketer)
        self.user = InternalHackleUser.builder().identifier("$id", "test_id").build()

    def test_식별자가_없는경우_False(self):
        # given
        experiment = create_experiment(identifier_type='custom_id')
        request = create_experiment_request(experiment=experiment, user=self.user)

        # when
        actual = self.sut.is_user_in_container_group(request, Mock())

        # then
        self.assertFalse(actual)

    def test_Bucket이_없으면_에러(self):
        # given
        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = None
        container = Container(1, 42, [])

        request = create_experiment_request(workspace=workspace, user=self.user)

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.is_user_in_container_group(request, container)

        # then
        self.assertEqual('Bucket[42]', str(actual.exception))

    def test_bucketing_결과_slot에_할당받지_않았으면_False(self):
        # given
        bucket = Mock(spec=Bucket)
        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = bucket
        container = Container(1, 42, [])

        self.bucketer.bucketing.return_value = None

        request = create_experiment_request(workspace=workspace, user=self.user)

        # when
        actual = self.sut.is_user_in_container_group(request, container)

        # then
        self.assertFalse(actual)

    def test_bucketing_결과에_해당하는_container_group_정보를_못찾는_경우_예외(self):
        # given
        bucket = Mock(spec=Bucket)
        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = bucket
        container = Container(1, 42, [])

        slot = Slot(0, 100, 320)
        self.bucketer.bucketing.return_value = slot

        request = create_experiment_request(workspace=workspace, user=self.user)

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.is_user_in_container_group(request, container)

        # then
        self.assertEqual('ContainerGroup[320]', str(actual.exception))

    def test_할당된_container_group에_실험이_없으면_False(self):
        # given
        bucket = Mock(spec=Bucket)
        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = bucket
        container = Container(1, 42, [ContainerGroup(320, [1000])])

        slot = Slot(0, 100, 320)
        self.bucketer.bucketing.return_value = slot

        experiment = create_experiment(id=999)
        request = create_experiment_request(workspace=workspace, experiment=experiment, user=self.user)

        # when
        actual = self.sut.is_user_in_container_group(request, container)

        # then
        self.assertFalse(actual)

    def test_할당된_container_group에_실험이_있으면_True(self):
        # given
        bucket = Mock(spec=Bucket)
        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = bucket
        container = Container(1, 42, [ContainerGroup(320, [999])])

        slot = Slot(0, 100, 320)
        self.bucketer.bucketing.return_value = slot

        experiment = create_experiment(id=999)
        request = create_experiment_request(workspace=workspace, experiment=experiment, user=self.user)

        # when
        actual = self.sut.is_user_in_container_group(request, container)

        # then
        self.assertTrue(actual)
