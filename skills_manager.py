#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from graph_models import *
import graphene

from graph_loader import load_makers, load_models, load_car_pricing, load_definitions


class Storage(object):
    db = {
        'makers': {},
        'models': {},
        'pricing': {},
        'definitions': {}
    }

    def get(self, domain, key):
        if not self.db.get(domain):
            if domain == 'makers':
                self.db[domain] = load_makers()
            elif domain == 'pricing':
                self.db[domain] = load_car_pricing()
            elif domain == 'definitions':
                self.db[domain] = load_definitions()
            elif domain == 'models':
                makers = self.db.get('makers')
                if not makers:
                    self.db['makers'] = load_makers()
                self.db[domain] = load_models(makers)
        return self.db[domain].get(key)


storage = Storage()


class QueryAPI(graphene.ObjectType):
    
    maker = graphene.Field(Maker,
                           brand=graphene.String()
                           )
    def resolve_maker(self, info, brand):
        return storage.get('makers', brand)

    makers = graphene.List(Maker,
                           maker1=graphene.String(),
                           maker2=graphene.String(),
                           )
    def resolve_makers(self, info, maker1, maker2):
        return [storage.get('makers', maker1), storage.get('makers', maker2)]

    model = graphene.Field(Model,
                           name=graphene.String(default_value=''),
                           trim=graphene.String(default_value=''),
                           series=graphene.String(default_value=''),
                           maker=graphene.String(default_value=''),
                           )
    def resolve_model(self, info, name, trim, series, maker):
        return Model(
            series=Series(
                name=series,
                maker=storage.get('models', 'porsche')
            )
        )

    pricing = graphene.Field(CarPricing,
                             maker=graphene.String(default_value=''),
                             fullname=graphene.String(default_value=''),
                             series=graphene.String(default_value=''),
                             trim=graphene.String(default_value=''),
                             body=graphene.String(default_value=''),
                             releasedDate=graphene.String(default_value=''),
                             transmissionDrivetrain=graphene.String(default_value=''),
                             transmissionType=graphene.String(default_value=''),
                             engineDisplacement=graphene.String(default_value=''),
                           )
    def resolve_pricing(self, info,
                        maker,
                        fullname,
                        series,
                        trim,
                        body,
                        releasedDate,
                        transmissionDrivetrain,
                        transmissionType,
                        engineDisplacement):
        items = storage.get('pricing', series)
        ite = None
        if items:
            for trim in items:
                ite_ = storage.get('pricing', fullname) or storage.get('pricing', trim)
                if ite_.transmission.drivetrain.lower() == transmissionDrivetrain:
                    ite = ite_
                    break

        if items and not ite:
            trim = items[0]
            ite = storage.get('pricing', trim)
        return ite

    comparePricing = graphene.List(CarPricing,
                                maker1=graphene.String(),
                                series1=graphene.String(),
                                maker2=graphene.String(),
                                series2=graphene.String(),
                             )
    def resolve_comparePricing(self, info, maker1, maker2, series1, series2):
        print('#resolve_comparePricing', maker1, series1, maker2, series2)
        return [
            storage.get('pricing', storage.get('pricing', series1)[0]),
            storage.get('pricing', storage.get('pricing', series2)[0])
        ]

    definition = graphene.Field(Definitions,
                                name=graphene.String())
    def resolve_definition(self, info, name):
        # print('#resolve_definition', name)
        return storage.get('definitions', name.lower())


class GraphQLManager(object):
    def __init__(self):
        self.scheme = graphene.Schema(query=QueryAPI)

    def invoke(self, invocation):

        query = invocation.get('graphql_query')
        variables = invocation.get('graphql_variables')

        # print(query, variables)

        result = self.scheme.execute(query, variable_values=variables)

        return result.data
