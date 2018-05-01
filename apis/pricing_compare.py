import graphene
from models import CarPricing


class ComparePricingAPI(graphene.ObjectType):
    comparePricing = graphene.List(CarPricing,
                                maker1=graphene.String(),
                                series1=graphene.String(),
                                maker2=graphene.String(),
                                series2=graphene.String(),
                             )
    def resolve_comparePricing(self, info, maker1, maker2, series1, series2):
        print('#resolve_comparePricing', maker1, series1, maker2, series2)
        return [
            info.context.storage.get('pricing', info.context.storage.get('pricing', series1)[0]),
            info.context.storage.get('pricing', info.context.storage.get('pricing', series2)[0])
        ]
