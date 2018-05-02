import graphene
from models import Model


class ModelsAPI(graphene.ObjectType):
    models = graphene.List(Model,
                           fullname=graphene.String(default_value=''),
                           series=graphene.String(default_value=''),
                           maker=graphene.String(default_value=''),
                           )
    def resolve_models(self, info, fullname, series, maker):
        s = info.context.storage
        result = s.get('models', fullname) or \
               s.get('models', series) or \
                 (not series and s.get('models', maker))

        if not result: return None

        return result if isinstance(result, list) else [result]
