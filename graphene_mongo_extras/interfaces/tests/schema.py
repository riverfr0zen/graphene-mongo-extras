import graphene
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from graphene_mongo_extras import MongoNodeInterface
from graphene.relay import Node, Connection
from graphene_mongo_extras import MongoNodeInterface, CountableConnectionBase
from graphene_mongo_extras.fields import InterfaceConnectionField
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


class ConnectionTestingToyInterface(MongoNodeInterface):
    """ Creating a separate class here just to show Meta options
    required for implementing as a Connection field """
    class Meta:
        model = Toy
        connection_class = CountableConnectionBase


class PlushieType(MongoengineObjectType):
    class Meta:
        model = Plushie
        interfaces = (ToyInterface, ConnectionTestingToyInterface)
        connection_class = Connection
        connection_field_class = MongoengineConnectionField


class VideogameType(MongoengineObjectType):
    class Meta:
        model = Videogame
        interfaces = (ToyInterface, ConnectionTestingToyInterface)
        connection_class = Connection
        connection_field_class = MongoengineConnectionField


class Query(graphene.ObjectType):
    toys = graphene.List(ToyInterface)

    def resolve_toys(self, info):
        return list(Toy.objects.all())

    all_toys_iface = InterfaceConnectionField(ConnectionTestingToyInterface)

    def resolve_all_toys_iface_old_way(self, info, **kwargs):
        return list(Toy.objects.all())


schema = graphene.Schema(
    query=Query,
    types=[PackagingType, PlushieType, VideogameType]
)
