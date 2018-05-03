import graphene
from models import Maker


class MakerAPI(graphene.ObjectType):

    app_key = {
        'invocation_id': 'nr1ylkb0jcy4pb',
        'client_secret': 'JdqCSvYC96Bz7jGS0NGABNTxEasx0IuI'
    }

    maker = graphene.Field(Maker,
                           brand=graphene.String()
                           )

    def resolve_maker(self, info, brand):
        return info.context.storage.get('makers', brand)