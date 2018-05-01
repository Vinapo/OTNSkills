import graphene
from models import Maker


class MakerAPI(graphene.ObjectType):
    maker = graphene.Field(Maker,
                           brand=graphene.String()
                           )

    def resolve_maker(self, info, brand):
        return info.context.storage.get('makers', brand)