import graphene
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from graphene_mongo_extras import MongoNodeInterface
from graphene.relay import Node, Connection
from graphene_mongo_extras import MongoNodeInterface
from graphene_mongo_extras.interfaces.tests.models import Toy, Packaging, \
                                                          Plushie, Videogame


class PackagingType(MongoengineObjectType):
    class Meta:
        model = Packaging
        interfaces = (Node,)
        connection_class = Connection
        connection_field_class = MongoengineConnectionField


class ToyInterface(MongoNodeInterface):
    class Meta:
        model = Toy


class PlushieType(MongoengineObjectType):
    class Meta:
        model = Plushie
        interfaces = (ToyInterface,)
        connection_class = Connection
        connection_field_class = MongoengineConnectionField


class VideogameType(MongoengineObjectType):
    class Meta:
        model = Videogame
        interfaces = (ToyInterface,)
        connection_class = Connection
        connection_field_class = MongoengineConnectionField


class PlushieNodeType(MongoengineObjectType):
    class Meta:
        model = Plushie
        interfaces = (ToyInterface,)
        connection_class = Connection
        connection_field_class = MongoengineConnectionField


class VideogameNodeType(MongoengineObjectType):
    class Meta:
        model = Videogame
        interfaces = (ToyInterface,)
        connection_class = Connection
        connection_field_class = MongoengineConnectionField


# @TODO unions
# class ToyUnion(graphene.Union):
#     class Meta:
#         types = (PlushieNodeType, VideogameNodeType)


# class ToyUnionConnection(graphene.Connection):
#     class Meta:
#         node = ToyUnion


class ToyInterfaceConnection(graphene.Connection):
    class Meta:
        node = ToyInterface


class Query(graphene.ObjectType):
    toys = graphene.List(ToyInterface)

    def resolve_toys(self, info):
        return list(Toy.objects.all())

    all_toys_iface = graphene.ConnectionField(ToyInterfaceConnection)

    def resolve_all_toys_iface(self, info, **kwargs):
        return list(Toy.objects.all())

    # @TODO unions
    # all_toys_union = graphene.ConnectionField(ToyUnionConnection)

    # def resolve_all_toys_union(self, info, **kwargs):
    #     return list(Toy.objects.all())


schema = graphene.Schema(
    query=Query,
    types=[PackagingType, PlushieType, VideogameType,
           PlushieNodeType, VideogameNodeType]
)
