import graphene
from models import Maker


class MakersAPI(graphene.ObjectType):

    app_key = {
        'invocation_id': '9bmaeo13dq8zfm',
        'client_secret': 'SyMU3oislb8AB6toOAPV8SwoTvNe3f46'
    }

    makers = graphene.List(Maker,
                           maker1=graphene.String(),
                           maker2=graphene.String(),
                           )

    def resolve_makers(self, info, maker1, maker2):
        return [info.context.storage.get('makers', maker1), info.context.storage.get('makers', maker2)]
