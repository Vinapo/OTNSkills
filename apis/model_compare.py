import graphene
from models import Model


class CompareModelsAPI(graphene.ObjectType):

    app_key = [
        {
            'invocation_id': '0hcc70hudadlz1',
            'client_secret': '93mJTXMTc4fJ5OhsJxAkyJEw35UDBS7a'
        },
        {
            'invocation_id': 'dd0ssvs3svbw6j',
            'client_secret': '1wuhDqeDDCj0RTjO0uwWuyEslMYZpytF'
        }
    ]

    compareModels = graphene.List(Model,
                             fullname1=graphene.String(default_value=''),
                             trim1=graphene.String(default_value=''),
                             series1=graphene.String(default_value=''),
                             body1=graphene.String(default_value=''),
                             releasedDate1=graphene.String(default_value=''),
                             transmissionDrivetrain1=graphene.String(default_value=''),
                             transmissionType1=graphene.String(default_value=''),
                             engineDisplacement1=graphene.String(default_value=''),
                             fullname2=graphene.String(default_value=''),
                             trim2=graphene.String(default_value=''),
                             series2=graphene.String(default_value=''),
                             body2=graphene.String(default_value=''),
                             releasedDate2=graphene.String(default_value=''),
                             transmissionDrivetrain2=graphene.String(default_value=''),
                             transmissionType2=graphene.String(default_value=''),
                             engineDisplacement2=graphene.String(default_value=''),
                             limit=graphene.Int(default_value=4),
                             )
    def resolve_compareModels(self, info,
                              fullname1,
                              trim1,
                              series1,
                              body1,
                              releasedDate1,
                              transmissionDrivetrain1,
                              transmissionType1,
                              engineDisplacement1,
                              fullname2,
                              trim2,
                              series2,
                              body2,
                              releasedDate2,
                              transmissionDrivetrain2,
                              transmissionType2,
                              engineDisplacement2,
                              limit
                        ):

        # print(limit)

        s = info.context.storage
        return [
            s.get('models', series1)[0],
            s.get('models', 'Mazda 3 Sedan 1.5L'),
        ]