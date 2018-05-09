import graphene
from graphql_models import Maker


class MakerAPI(graphene.ObjectType):

    app_key = {
        'invocation_id': 'nr1ylkb0jcy4pb',
        'client_secret': 'JdqCSvYC96Bz7jGS0NGABNTxEasx0IuI'
    }

    '''
     query($CAR_MAKER1:String!) {
        maker (brand: $CAR_MAKER1) {
            brand
            name
            found
            founder
            nativeName
            description
            revenue
            netIncome
            logo {
                url
            }
            divisions
            shareholders {
                name
                share
            }
            image {
                url
                description
            }
            sales {
                year
                units
                rank
            }
          }
        }
    '''

    maker = graphene.Field(Maker,
                           brand=graphene.String()
                           )

    def resolve_maker(self, info, brand):

        cache = info.context.cache

        prefix = 'maker-'
        key = '%s%s' % (prefix, brand)

        # cache.delete(key)

        def f(x):
            return info.context.storage.get('makers', x[len(prefix):])

        return cache.get(key, ex=3600, callback=f) if cache else f(brand)
