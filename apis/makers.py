import graphene
from models import Maker


class MakersAPI(graphene.ObjectType):
    makers = graphene.List(Maker,
                           maker1=graphene.String(),
                           maker2=graphene.String(),
                           )

    def resolve_makers(self, info, maker1, maker2):
        return [info.context.storage.get('makers', maker1), info.context.storage.get('makers', maker2)]
