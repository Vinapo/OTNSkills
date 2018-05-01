import graphene
from models import Definitions


class DefinitionsAPI(graphene.ObjectType):
    definition = graphene.Field(Definitions,
                                name=graphene.String())
    def resolve_definition(self, info, name):
        return info.context.storage.get('definitions', name.lower())

