import graphene
from graphql_models import Definitions


class DefinitionsAPI(graphene.ObjectType):

    app_key = {
        'invocation_id': 'ghnwbonioo9nzc',
        'client_secret': 'VwpPXOf28XaPi8ZzRcLvnSeIjGFzoyGt'
    }

    '''
    query($DEF1__definition_of:String!){
        definition(name: $DEF1__definition_of){
            name,
            title,
            content,
            source{
                url
                description
            }
            image{
                url
                description
            }
        }
    }
    '''

    definition = graphene.Field(Definitions,
                                name=graphene.String())
    def resolve_definition(self, info, name):
        return info.context.storage.get('definitions', name.lower())

