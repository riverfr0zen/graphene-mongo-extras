import pytest
import graphene
from graphene.test import Client
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from graphene_mongo_extras import MongoengineInterface
from graphene.relay import Node, Connection
from graphene_mongo_extras.interfaces.tests.models import Toy, Packaging, \
                                                          Plushie, Videogame


@pytest.fixture
def cleanup():
    yield
    Toy.drop_collection()
    Packaging.drop_collection()


@pytest.fixture
def setup_data():
    fifipak = Packaging(name="FifiPak").save()
    Plushie(name="fifi", animal="dog",
            packaging=fifipak).save()
    kittypak = Packaging(name="KittyPak").save()
    Plushie(name="kitty", animal="cat",
            packaging=kittypak).save()
    contrapak = Packaging(name="ContraPak").save()
    Videogame(name="Contra", genre="shmup",
              packaging=contrapak).save()
    dspak = Packaging(name="DSPak").save()
    Videogame(name="Dark Souls", genre="masochism",
              packaging=dspak).save()


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
        interfaces = (Node, ToyInterface,)
        # interfaces = (ToyInterface,)
        connection_class = Connection
        connection_field_class = MongoengineConnectionField


class VideogameType(MongoengineObjectType):
    class Meta:
        model = Videogame
        interfaces = (Node, ToyInterface,)
        # interfaces = (ToyInterface,)
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


def test_mongoengine_interface(setup_data, cleanup):

    client = Client(schema)
    res = client.execute('''{
        toys {
            name
            packaging {
                name
            }
            ... on PlushieType {
                animal
            }
            ... on VideogameType {
                genre
            }
        }
    }''')
    assert len(res['data']['toys']) == 4
    assert 'packaging' in res['data']['toys'][0]
    assert res['data']['toys'][0]['packaging']['name'] == 'FifiPak'
    assert 'animal' in res['data']['toys'][0]
    assert res['data']['toys'][0]['animal'] == 'dog'
    assert res['data']['toys'][1]['packaging']['name'] == 'KittyPak'
    assert 'animal' in res['data']['toys'][1]
    assert res['data']['toys'][1]['animal'] == 'cat'
    assert res['data']['toys'][2]['packaging']['name'] == 'ContraPak'
    assert 'genre' in res['data']['toys'][2]
    assert res['data']['toys'][2]['genre'] == 'shmup'
    assert res['data']['toys'][3]['packaging']['name'] == 'DSPak'
    assert 'genre' in res['data']['toys'][3]
    assert res['data']['toys'][3]['genre'] == 'masochism'
