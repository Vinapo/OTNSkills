import graphene
from graphql_models import Model


class ModelAPI(graphene.ObjectType):

    app_key = {
        'invocation_id': 'ocx3z17z2qyys7',
        'client_secret': '2SfCm4Iy2LN0LpbyxPLjpcJV7ARPPdr4'
    }

    model = graphene.Field(Model,
                           fullname=graphene.String(),
                           )
    def resolve_model(self, info, fullname):
        s = info.context.storage
        result = s.get('models', fullname)

        return result


if __name__ == '__main__':

    from graphql_models import *

    scheme = graphene.Schema(query=ModelAPI)

    query = '''
        query($CAR1_Fullname:String!){
        model(fullname:$CAR1_Fullname){
            fullname
            bodyType
        }
    }
    '''
    variables = {
        'CAR1_Fullname': 'mazda 3 hatchback'
    }

    # print(query, variables)

    class QueryAPIContext(object):
        storage = {
            'models':
                Model(
                    fullname='Mazda 3 Hatchback',
                    bodyType=BodyType.sedan.value
                )
        }


    result = scheme.execute(query,
                            variable_values=variables,
                            context_value=QueryAPIContext()
                            )

    print(result.data)

