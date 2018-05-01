#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import graphene
import pkgutil
import importlib
from loader import Storage


class QueryAPIContext(object):
    storage = Storage()


class GraphQLManager(object):
    def __init__(self):

        apis = []
        folder = 'apis'
        for (module_loader, name, ispkg) in pkgutil.iter_modules([folder]):
            mod = importlib.import_module(folder + '.' + name)
            for cls in mod.__dict__.keys():
                if cls[-3:] != 'API': continue
                cls = getattr(mod, cls)
                apis.append(cls)

        Query = type('Query', tuple(apis), {})

        self.scheme = graphene.Schema(query=Query)

        self.context = QueryAPIContext()

    def invoke(self, invocation):

        query = invocation.get('graphql_query')
        variables = invocation.get('graphql_variables')

        # print(query, variables)

        result = self.scheme.execute(query,
                                     variable_values=variables,
                                     context_value=self.context)

        return result.data
