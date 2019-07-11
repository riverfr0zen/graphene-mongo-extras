import pytest
from graphene.test import Client
from graphene_mongo_extras.interfaces.tests.models import Toy, Packaging, \
                                                          Plushie, Videogame
from graphene_mongo_extras.interfaces.tests.schema import schema


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
    assert 'data' in res
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
