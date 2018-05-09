import graphene
from graphql_models import Model, Series, Maker


class WheelSizeAPI(graphene.ObjectType):

    app_key = {
        'invocation_id': 'd90825vvgiww92',
        'client_secret': 'FhCcwJxjBdFLRjtxHBTTpG2hzEG0wVj7'
    }

    wheelSize = graphene.Field(Model,
                                series=graphene.String())
    def resolve_wheelSize(self, info, series):
        return Model(
            fullname='Mazda 3 Hatchback',
            wheelSize=17.0,
            series=Series(
                name='Mazda 3',
                maker=Maker(
                    name='Mazda'
                )
            )
        )

