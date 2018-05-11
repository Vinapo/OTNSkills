#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function  # Python 2/3 compatibility
from adapters.neptune import Neptune
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import *
import unittest


class GraphQueryTest(unittest.TestCase):
    def setUp(self):
        self.nep = Neptune('ws://ec2-54-89-143-194.compute-1.amazonaws.com:8182/gremlin')

    def test_query_car_maker(self):
        g = self.nep.g
        result = g.V().hasLabel("CarMaker")\
                      .properties("name")\
                      .toList()
        print(result)

    def test_query_car_by_made_by(self):
        g = self.nep.g
        result = g.V().hasLabel("CarMaker")\
                      .has("_name", "mazda")\
                      .inE("made_by")\
                      .outV()\
                      .inE("attr")\
                      .has("name","series")\
                      .outV().dedup()\
                      .values("fullname")\
                      .toList()
        print(result)

    def test_query_car_by_name(self):
        g = self.nep.g
        result = g.V().hasLabel("Car")\
                      .has("name", "morning")\
                      .values("fullname")\
                      .toList()
        print(result)

    def test_query_car_similar(self):
        g = self.nep.g
        result = g.V().hasLabel("Car")\
                      .has("name", "mazda 3")\
                      .outE('similar')\
                      .inV()\
                      .values("fullname")\
                      .toList()

        print(result)

    def test_query_car_by_price(self):
        g = self.nep.g
        result = g.V().hasLabel("Car")\
                      .and_(
                        __.has('price', gt(450*1e6)),
                        __.has('price', lt(550*1e6)))\
                      .values("fullname")\
                      .toList()
        print(result)

    def test_query_car_price(self):
        g = self.nep.g
        result = g.V().hasLabel("Car")\
                      .has("name", "mazda 3 sedan")\
                      .values("price")\
                      .toList()
        print(result)

    def test_query_car_by_purpose(self):
        g = self.nep.g
        result = g.V().hasLabel("Car")\
                      .and_(
                        __.has("purposes", "family"),
                        __.has("num_seats", 7))\
                      .values("fullname")\
                      .toList()
        print(result)