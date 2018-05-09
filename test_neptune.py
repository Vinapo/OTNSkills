from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from pprint import pprint

graph = Graph()
conn = DriverRemoteConnection('ws://54.89.143.194:8182/gremlin','g')
g = graph.traversal().withRemote(conn)

# mazda 3 hatchback car model query
result = g.V().hasLabel("Car").has("name", "mazda 3 hatchback").valueMap().toList()
[pprint(v) for v in result]

# mazda car maker query
result = g.V().hasLabel("CarMaker").has("name", "mazda").valueMap().toList()
print(result)

# query 5 xe: xe 5 cho
result = g.V().hasLabel("Car").has("num_seats", 5).limit(10).values("fullname").toList()
print(result)

