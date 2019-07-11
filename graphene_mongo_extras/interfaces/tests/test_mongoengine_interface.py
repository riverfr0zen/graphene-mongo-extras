import pytest
from bson.objectid import ObjectId
from graphql_relay import from_global_id, to_global_id
from graphene.test import Client
from graphene_mongo_extras.interfaces.tests.models import Toy, Packaging, \
                                                          Plushie, Videogame
from graphene_mongo_extras.interfaces.tests.schema import schema


@pytest.fixture
def setup_data():
    fifipak = Packaging(name="FifiPak").save()
    fifi = Plushie(name="fifi", animal="dog",
                   packaging=fifipak).save()
    kittypak = Packaging(name="KittyPak").save()
    kitty = Plushie(name="kitty", animal="cat",
                    packaging=kittypak).save()
    contrapak = Packaging(name="ContraPak").save()
    contra = Videogame(name="Contra", genre="shmup",
                       packaging=contrapak).save()
    dspak = Packaging(name="DSPak").save()
    ds = Videogame(name="Dark Souls", genre="masochism",
                   packaging=dspak).save()
    yield {
        'fifipak': fifipak,
        'fifi': fifi,
        'kittypak': kittypak,
        'kitty': kitty,
        'contrapak': contrapak,
        'contra': contra,
        'dspak': dspak,
        'ds': ds
    }
    # Cleanup
    Toy.drop_collection()
    Packaging.drop_collection()


def test_mongoengine_interface(setup_data):

    client = Client(schema)
    res = client.execute('''{
        toys {
            id
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
    d_fifi = res['data']['toys'][0]
    d_fifi_type, d_fifi_id = from_global_id(d_fifi['id'])
    assert d_fifi_type == 'PlushieType'
    assert d_fifi_id == str(setup_data['fifi'].pk)
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
