from hackle.internal.workspace.workspace import Workspace
from tests.resources.test_resource_reader import read_resource


class ResourceWorkspaceFetcher(object):

    def __init__(self, file_name):
        data = read_resource(file_name)
        self.__workspace = Workspace(data)

    def fetch(self):
        return self.__workspace
