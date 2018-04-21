#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from graph_models import *
import graphene

from graph_loader import load_makers, load_models


MAKERS = load_makers()
MODELS = load_models(MAKERS)


class QueryAPI(graphene.ObjectType):

    maker = graphene.Field(Maker,
                           brand=graphene.String()
                           )
    def resolve_maker(self, info, brand):
        return MAKERS.get(brand)

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
                maker=MAKERS.get('porsche')
            )
        )

    pricing = graphene.Field(CarPricing,
                           series=graphene.String(default_value=''),
                           trim=graphene.String(default_value=''),
                           )

    def resolve_pricing(self, info, series, trim):
        print(series, trim)
        if series == 'cx-5':
            return CarPricing(
                trim='Mazda CX-5',
                price=12345,
                rolling_price=12346,
            )
        else:
            return CarPricing(
                trim='Macan',
                price=22345,
                rolling_price=22346,
            )



class GraphQLManager(object):
    def __init__(self):
        self.scheme = graphene.Schema(query=QueryAPI)

    def invoke(self, invocation):

        query = invocation.get('graphql_query')
        variables = invocation.get('graphql_variables')

        result = self.scheme.execute(query, variable_values=variables)

        return result.data
