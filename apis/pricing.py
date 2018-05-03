import graphene
from models import CarPricing


class PricingAPI(graphene.ObjectType):

    app_key = [
        {
            'invocation_id': 'u0ma9p6lmhejbf',
            'client_secret': 'wZe8fenKvzNfVsRNY8ERnCYdMPiZQ0Kj'
        },
        {
            'invocation_id': 'mj9zmlpqxh92tz',
            'client_secret': 'uLzFZXW0sqOUTiOxDVfycrR9CZ62MTt6'
        }
    ]

    pricing = graphene.Field(CarPricing,
                             maker=graphene.String(default_value=''),
                             fullname=graphene.String(default_value=''),
                             trim=graphene.String(default_value=''),
                             series=graphene.String(default_value=''),
                             body=graphene.String(default_value=''),
                             releasedDate=graphene.String(default_value=''),
                             transmissionDrivetrain=graphene.String(default_value=''),
                             transmissionType=graphene.String(default_value=''),
                             engineDisplacement=graphene.String(default_value=''),
                             atPlace=graphene.String(default_value='')
                           )
    def resolve_pricing(self, info,
                        maker,
                        fullname,
                        trim,
                        series,
                        body,
                        releasedDate,
                        transmissionDrivetrain,
                        transmissionType,
                        engineDisplacement,
                        atPlace):
        print(fullname)
        items = info.context.storage.get('pricing', series)
        ite = None
        if items:
            for trim in items:
                ite_ = info.context.storage.get('pricing', fullname) or info.context.storage.get('pricing', trim)
                if ite_.transmission.drivetrain.lower() == transmissionDrivetrain:
                    ite = ite_
                    break

        if items and not ite:
            fullname = items[0]
            ite = info.context.storage.get('pricing', fullname)
        return ite