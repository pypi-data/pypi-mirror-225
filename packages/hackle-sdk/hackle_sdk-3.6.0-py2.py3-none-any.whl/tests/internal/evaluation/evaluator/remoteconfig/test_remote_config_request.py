from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_request import RemoteConfigRequest
from hackle.internal.model.entities import RemoteConfigParameter, RemoteConfigParameterValue
from hackle.internal.user.identifier_type import IdentifierType
from hackle.internal.user.internal_hackle_user import InternalHackleUser
from hackle.internal.workspace.workspace import Workspace


def create_remote_config_request(**params):
    return RemoteConfigRequest(
        workspace=params.get('workspace', Workspace('{}')),
        user=params.get('user', InternalHackleUser.builder().identifier(IdentifierType.ID, 'user').build()),
        parameter=params.get('parameter', RemoteConfigParameter(1, 'key', 'STRING', IdentifierType.ID, [],
                                                                RemoteConfigParameterValue(1, 'defaultValue'))),
        required_type=params.get('required_type', 'STRING'),
        default_value=params.get('default_value', 'default value')
    )
