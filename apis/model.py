import graphene
from models import Model, Series


class ModelAPI(graphene.ObjectType):
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
                maker=info.context.storage.get('models', 'porsche')
            )
        )
