import graphene
from models import CarPricing


class PricingAPI(graphene.ObjectType):
    pricing = graphene.Field(CarPricing,
                             maker=graphene.String(default_value=''),
                             fullname=graphene.String(default_value=''),
                             series=graphene.String(default_value=''),
                             trim=graphene.String(default_value=''),
                             body=graphene.String(default_value=''),
                             releasedDate=graphene.String(default_value=''),
                             transmissionDrivetrain=graphene.String(default_value=''),
                             transmissionType=graphene.String(default_value=''),
                             engineDisplacement=graphene.String(default_value=''),
                           )
    def resolve_pricing(self, info,
                        maker,
                        fullname,
                        series,
                        trim,
                        body,
                        releasedDate,
                        transmissionDrivetrain,
                        transmissionType,
                        engineDisplacement):
        items = info.context.storage.get('pricing', series)
        ite = None
        if items:
            for trim in items:
                ite_ = info.context.storage.get('pricing', fullname) or info.context.storage.get('pricing', trim)
                if ite_.transmission.drivetrain.lower() == transmissionDrivetrain:
                    ite = ite_
                    break

        if items and not ite:
            trim = items[0]
            ite = info.context.storage.get('pricing', trim)
        return ite