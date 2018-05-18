import graphene
from graphql_models import *
import adapters.aurora as a
import json


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

        # cache = info.context.cache
        #
        # prefix = 'maker-'
        # key = '%s%s' % (prefix, brand)
        #
        # # cache.delete(key)
        #
        # def f(x):
        #     return info.context.storage.get('makers', x[len(prefix):])
        #
        # return cache.get(key, ex=3600, callback=f) if cache else f(key)

        session = info.context.session
        # session()

        try:
            maker = session.query(a.Maker).filter(
                a.Maker.brand == brand
            ).first()

            if not maker: return None

            sales = session.query(a.Sales).filter(
                a.Sales.name == brand
            )
        except:
            session.rollback()

        # session.remove()

        return Maker(
            brand=maker.brand,
            name=maker.name,
            nativeName=maker.native_name,
            found=maker.found,
            founder=[People(name=v) for v in json.loads(maker.founder)],
            revenue=maker.revenue,
            netIncome=maker.net_income,
            description=maker.description,
            shareholders=[Organization(name=v[0], share='%s%%' % v[1]) for v in json.loads(maker.shareholders)],
            divisions=[Organization(name=v) for v in json.loads(maker.divisions)],
            subsidiaries=maker.subsidiaries,
            website=Source(url=maker.website),
            logo=Source(url=maker.logo),
            image=Source(
                url=maker.image,
                description=maker.image_description
            ),
            sales=[Sales(
                year=sale.date.year,
                units=sale.units,
                rank=sale.rank
            ) for sale in sales]
        )
