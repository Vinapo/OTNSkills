import graphene
from models import Model


class CompareModelsAPI(graphene.ObjectType):

    app_key = {
        'invocation_id': '0hcc70hudadlz1',
        'client_secret': '93mJTXMTc4fJ5OhsJxAkyJEw35UDBS7a'
    }

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
                              engineDisplacement2
                        ):
        return [
            info.context.storage.get('models', series1),
            info.context.storage.get('models', series2)
        ]