#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import graphene
import pkgutil
import importlib
from loader import Storage
import ConfigParser, os
from adapters.elasticache import ElastiCache
from adapters.aurora import scoped_session, create_session


class QueryAPIContext(object):
    def __init__(self):
        self.storage = Storage()

        self.settings = ConfigParser.ConfigParser()

        self.settings.readfp(
            open((os.environ.get('STAGE') or 'development') + '.ini')
        )

        host = self.settings.get('app:main', 'aws.redis.host')
        if host:
            self.cache = ElastiCache(
                host=host,
                port=self.settings.get('app:main', 'aws.redis.port')
            )
        else:
            self.cache = {}

        self.session = scoped_session(create_session(host=self.settings.get('app:main', 'aws.aurora')))


class GraphQLManager(object):
    def __init__(self):

        self.app_keys = {}

        apis = []
        folder = 'apis'
        for (module_loader, name, ispkg) in pkgutil.iter_modules([folder]):
            mod = importlib.import_module(folder + '.' + name)
            for cls in mod.__dict__.keys():
                if cls[-3:] != 'API': continue
                cls = getattr(mod, cls)
                try:
                    app_key = getattr(cls, 'app_key')
                    if not isinstance(app_key, list):
                        app_key = [app_key]
                    for key in app_key:
                        self.app_keys[key.get('invocation_id')] = key.get('client_secret')
                except:
                    pass
                apis.append(cls)

        Query = type('Query', tuple(apis), {})

        self.scheme = graphene.Schema(query=Query)

        self.context = QueryAPIContext()

    def invoke(self, invocation):

        query = invocation.get('graphql_query')
        variables = invocation.get('graphql_variables')

        # print(query, variables)

        self.context.session()
        result = self.scheme.execute(query,
                                     variable_values=variables,
                                     context_value=self.context)
        self.context.session.remove()
        return result.data
