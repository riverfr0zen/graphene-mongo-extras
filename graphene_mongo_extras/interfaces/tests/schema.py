import graphene
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from graphene_mongo_extras import MongoengineInterface
from graphene.relay import Node, Connection
from graphene_mongo_extras.interfaces.tests.models import Toy, Packaging, \
                                                          Plushie, Videogame


class ToyInterface(MongoengineInterface):
    class Meta:
        model = Toy


class PackagingType(MongoengineObjectType):
    class Meta:
        model = Packaging
        interfaces = (Node,)
        connection_class = Connection
        connection_field_class = MongoengineConnectionField


class PlushieType(MongoengineObjectType):
    class Meta:
        model = Plushie
        # interfaces = (Node, ToyInterface,)
        interfaces = (ToyInterface,)
        connection_class = Connection
        connection_field_class = MongoengineConnectionField


class VideogameType(MongoengineObjectType):
    class Meta:
        model = Videogame
        # interfaces = (Node, ToyInterface,)
        interfaces = (ToyInterface,)
        connection_class = Connection
        connection_field_class = MongoengineConnectionField


class Query(graphene.ObjectType):
    toys = graphene.List(ToyInterface)

    def resolve_toys(self, info):
        return list(Toy.objects.all())


schema = graphene.Schema(
    query=Query,
    types=[PackagingType, PlushieType, VideogameType]
)
