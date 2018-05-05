
from __future__  import print_function  # Python 2/3 compatibility

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

graph = Graph()

g = graph.traversal().withRemote(DriverRemoteConnection('ws://54.89.143.194:8182/gremlin','g'))

print(g.V().limit(10).toList())
