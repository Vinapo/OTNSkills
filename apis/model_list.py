import graphene
from models import Model


class ModelsAPI(graphene.ObjectType):

    app_key = [
        {
            'invocation_id': 'peua9209vvyb72',
            'client_secret': 'oyJniEVX2JIPLqtNB1MqhCBOXqOsgZpU'
        },
        {
            'invocation_id': 'bf544daqnr1x9a',
            'client_secret': 'VuhB7K01c7z8jSnSIVnjoHYrXrnAUcoM'
        }
    ]

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
