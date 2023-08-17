from hackle.internal.evaluation.evaluator.experiment.experiment_request import ExperimentRequest
from hackle.internal.user.internal_hackle_user import InternalHackleUser
from hackle.internal.workspace.workspace import Workspace
from tests.internal.model.test_entities import create_experiment


def create_experiment_request(workspace=None, user=None, experiment=None, default_variation_key='A'):
    return ExperimentRequest.of(
        workspace=workspace or Workspace('{}'),
        user=user or InternalHackleUser(identifiers={'$id': 'user'}, properties={}),
        experiment=experiment or create_experiment(),
        default_variation_key=default_variation_key
    )
