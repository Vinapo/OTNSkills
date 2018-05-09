import graphene
from graphql_models import Model


class ModelAPI(graphene.ObjectType):

    app_key = {
        'invocation_id': 'ocx3z17z2qyys7',
        'client_secret': '2SfCm4Iy2LN0LpbyxPLjpcJV7ARPPdr4'
    }

    model = graphene.Field(Model,
                           fullname=graphene.String(),
                           )
    def resolve_model(self, info, fullname):
        s = info.context.storage
        result = s.get('models', fullname)
        return result


