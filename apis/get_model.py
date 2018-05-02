import graphene
from models import Model


class ModelAPI(graphene.ObjectType):
    model = graphene.Field(Model,
                           fullname=graphene.String(),
                           )
    def resolve_model(self, info, fullname):
        s = info.context.storage
        result = s.get('models', fullname)
        return result


