import os
from unittest import TestCase

from hackle.internal.workspace.workspace import Workspace


class WorkspaceTest(TestCase):

    def test_workspace_fetch(self):
        with open(os.path.join(os.path.dirname(__file__), '../../resources/workspace_config.json'), 'r') as f:
            data = f.read()
        workspace = Workspace(data)
        self.assertIsNotNone(workspace)
        self.assertTrue(bool(workspace.bucket_id_map))
        self.assertTrue(bool(workspace.event_type_key_map))
        self.assertTrue(bool(workspace.experiment_key_map))
        self.assertTrue(bool(workspace.feature_flag_key_map))
        self.assertTrue(bool(workspace.parameter_configurations))
        self.assertTrue(bool(workspace.remote_config_parameters))
        self.assertTrue(bool(workspace.segment_key_map))
