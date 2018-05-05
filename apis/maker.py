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
        cache = info.context.cache

        def f(x):
            return info.context.storage.get('makers', x)

        if cache:
            return cache.get(brand, ex=3000, callback=f)

        return f(brand)