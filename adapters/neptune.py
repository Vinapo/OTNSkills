from __future__ import print_function  # Python 2/3 compatibility
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


class Neptune(object):
    def __init__(self, uri):
        """

        :param uri: example 'ws://54.89.143.194:8182/gremlin'
        """
        self.graph = Graph()
        self.g = self.graph.traversal().withRemote(DriverRemoteConnection(uri,'g'))