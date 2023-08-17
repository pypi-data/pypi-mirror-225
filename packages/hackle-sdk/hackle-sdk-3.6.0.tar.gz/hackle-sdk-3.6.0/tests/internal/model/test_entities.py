from hackle.internal.model.entities import Experiment, Variation, TargetAction, RemoteConfigParameter, \
    RemoteConfigParameterValue


def create_experiment(**params):
    """
    :rtype: Experiment
    """
    return Experiment(
        id=params.get("id", 1),
        key=params.get("key", 1),
        type=params.get("type", "AB_TEST"),
        identifier_type=params.get("identifier_type", '$id'),
        status=params.get('status', 'RUNNING'),
        version=params.get('version', 1),
        execution_version=params.get('execution_version', 1),
        variations=params.get("variations", [create_variation(id=1, key="A"), create_variation(id=2, key="B")]),
        user_overrides=params.get("user_overrides", {}),
        segment_overrides=params.get('segment_overrides', []),
        target_audiences=params.get('target_audiences', []),
        target_rules=params.get('target_rules', []),
        default_rule=params.get('default_rule', TargetAction('BUCKET', bucket_id=1)),
        container_id=params.get('container_id'),
        winner_variation_id=params.get('winner_variation_id')
    )


def create_variation(**params):
    """
    :rtype: Variation
    """
    return Variation(
        id=params.get("id", 1),
        key=params.get("key", "A"),
        is_dropped=params.get("is_dropped", False),
        parameter_configuration_id=params.get("config_id")
    )


def create_parameter(**params):
    """
    :rtype: RemoteConfigParameter
    """
    return RemoteConfigParameter(
        id=params.get("id", 1),
        key=params.get('key', 'test_parameter_key'),
        type=params.get("type', 'STRING"),
        identifier_type=params.get("identifier_type", '$id'),
        target_rules=params.get('target_rules', []),
        default_value=params.get('default_value', RemoteConfigParameterValue(1, 'parameter_default'))
    )
