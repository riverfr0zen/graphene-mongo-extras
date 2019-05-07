import pytest
import graphene
from graphql_relay.node.node import to_global_id
from graphene.relay import Node
from datetime import datetime
from .. import FiltersRegistry
from ..fields import FilteringConnectionField
#from graphene_mongo import MongoengineObjectType
from graphene_mongo_extras import MongoengineExtrasType
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField,
    StringField,
    IntField,
    EmbeddedDocumentField,
)


class PlaythruInfo(EmbeddedDocument):
    difficulty = StringField()
    continues = IntField()


class HighScore(Document):
    player = StringField()
    score = IntField()
    recorded = DateTimeField()
    info = EmbeddedDocumentField(PlaythruInfo)


@pytest.fixture
def setup_data(setup_mongo):
    HighScore.drop_collection()
    yield [
        HighScore(player="liz", score=5, recorded=datetime(2019, 1, 1),
                  info=PlaythruInfo(difficulty="easy", continues=2)).save(),
        HighScore(player="bob", score=1, recorded=datetime(2019, 1, 1),
                  info=PlaythruInfo(difficulty="easy", continues=3)).save(),
        HighScore(player="boo", score=5, recorded=datetime(2019, 1, 2),
                  info=PlaythruInfo(difficulty="medium", continues=1)).save(),
        HighScore(player="jim", score=7, recorded=datetime(2019, 1, 3),
                  info=PlaythruInfo(difficulty="medium", continues=0)).save(),
        HighScore(player="zin", score=8, recorded=datetime(2019, 1, 3),
                  info=PlaythruInfo(difficulty="hard", continues=2)).save(),
        HighScore(player="jen", score=10, recorded=datetime(2019, 1, 3),
                  info=PlaythruInfo(difficulty="hard", continues=0)).save(),
        HighScore(player="dav", score=10, recorded=datetime(2019, 1, 5),
                  info=PlaythruInfo(difficulty="hard", continues=1)).save(),
        HighScore(player="sam", score=1, recorded=datetime(2019, 1, 5),
                  info=PlaythruInfo(difficulty="medium", continues=1)).save(),
    ]
    # Teardown
    HighScore.drop_collection()


class HighScoreType(MongoengineExtrasType):
    class Meta:
        model = HighScore
        interfaces = (Node,)
        connection_field_class = FilteringConnectionField


class Query(graphene.ObjectType):
    highscores = FilteringConnectionField(HighScoreType)


schema = graphene.Schema(
    query=Query,
    types=[
        HighScoreType,
    ]
)


def test_filterset_depth():
    import logging
    logging.debug(dir(FiltersRegistry._registry['HighScoreFilterset']))


def test_order_by(setup_data):
    field = FilteringConnectionField(HighScoreType)
    connection = field.default_resolver(None, {}, order_by='-player')
    objs = connection.iterable
    assert objs[0].player == "zin"
    assert objs[7].player == "bob"

    field = FilteringConnectionField(HighScoreType)
    connection = field.default_resolver(None,
                                        {},
                                        order_by='-recorded, +score')
    objs = connection.iterable
    assert objs[0].player == "sam"
    assert objs[1].player == "dav"
    assert objs[2].player == "jim"
    assert objs[3].player == "zin"
    assert objs[4].player == "jen"

    field = FilteringConnectionField(HighScoreType)
    connection = field.default_resolver(None,
                                        {},
                                        order_by='-recorded, -score')
    objs = connection.iterable
    assert objs[0].player == "dav"
    assert objs[1].player == "sam"
    assert objs[2].player == "jen"
    assert objs[3].player == "zin"
    assert objs[4].player == "jim"


def test_existing_filter_by_id(setup_data):
    """ Testing that existing MongoengineConnectionField id filtering
    still works """
    field = FilteringConnectionField(HighScoreType)
    davs_id = to_global_id('HighScoreType', setup_data[6].id)
    connection = field.default_resolver(None, {}, id=davs_id)
    objs = connection.iterable
    assert objs.count() == 1
    assert objs[0].id == setup_data[6].id


def test_existing_filtering_equality(setup_data):
    """ Testing that existing MongoengineConnectionField equality
    filtering still works """
    field = FilteringConnectionField(HighScoreType)
    connection = field.default_resolver(None,
                                        {},
                                        score=10,
                                        recorded=datetime(2019, 1, 3))
    objs = connection.iterable
    assert objs.count() == 1
    assert objs[0].player == "jen"


def test_basic_filtering(setup_data):
    filtering_opt = {
        "op": "AND",
        "filters": [
            {"player__icontains": "bo"}
        ]
    }

    field = FilteringConnectionField(HighScoreType)
    connection = field.default_resolver(None,
                                        {},
                                        filtering=filtering_opt)
    objs = connection.iterable
    assert objs.count() == 2

    filtering_opt = {
        "op": "OR",
        "filters": [
            {"player__icontains": "ji"},
            {"player__icontains": "je"}
        ]
    }

    field = FilteringConnectionField(HighScoreType)
    connection = field.default_resolver(None,
                                        {},
                                        filtering=filtering_opt)
    objs = connection.iterable
    assert objs.count() == 2

    filtering_opt = {
        "op": "OR",
        "filters": [
            {"player__icontains": "ji",
             "score__gte": 10},
            {"player__icontains": "je"},
        ]
    }

    field = FilteringConnectionField(HighScoreType)
    connection = field.default_resolver(None,
                                        {},
                                        filtering=filtering_opt)
    objs = connection.iterable
    assert objs.count() == 3


def test_filtering_plus_regular_args(setup_data):
    field = FilteringConnectionField(HighScoreType)
    filtering_opt = {
        "op": "AND",
        "filters": [
            {"player__icontains": "j"},
        ]
    }
    connection = field.default_resolver(None,
                                        {},
                                        score=10,
                                        filtering=filtering_opt)
    objs = connection.iterable
    assert objs.count() == 1
    assert objs[0].player == "jen"


def test_advanced_filtering(setup_data):
    filtering_opt = {
        "op": "OR",
        "filters": [
            {"score__lt": 2},
            {"player__icontains": "zi"}
        ],
        "filtersets": [
            {
                "op": "AND",
                "filters": [
                    {"score__gte": 10},
                    {"player__icontains": "je"}
                ]
            }
        ]
    }

    field = FilteringConnectionField(HighScoreType)
    connection = field.default_resolver(None,
                                        {},
                                        filtering=filtering_opt)
    objs = connection.iterable.order_by('score', 'name')
    assert objs.count() == 4
    assert objs[0].player == "bob"
    assert objs[1].player == "sam"
    assert objs[2].player == "zin"
    assert objs[3].player == "jen"

    # essentially the same logic as previous, just formed differently
    filtering_opt = {
        "op": "OR",
        "filtersets": [
            {
                "op": "OR",
                "filters": [
                    {"score__lt": 2},
                    {"player__icontains": "zi"}
                ]
            },
            {
                "op": "AND",
                "filters": [
                    {"score__gte": 10},
                    {"player__icontains": "je"}
                ]
            }
        ]
    }

    field = FilteringConnectionField(HighScoreType)
    connection = field.default_resolver(None,
                                        {},
                                        filtering=filtering_opt)
    objs = connection.iterable.order_by('score', 'name')
    assert objs.count() == 4
    assert objs[0].player == "bob"
    assert objs[1].player == "sam"
    assert objs[2].player == "zin"
    assert objs[3].player == "jen"

    filtering_opt = {
        "op": "AND",
        "filtersets": [
            {
                "op": "OR",
                "filters": [
                    {"player__icontains": "bo"},
                    {"player__icontains": "j"}
                ]
            },
            {
                "op": "OR",
                "filters": [
                    {"score__lte": 1},
                    {"score__gte": 10},
                ]
            }
        ]
    }
    connection = field.default_resolver(None,
                                        {},
                                        filtering=filtering_opt)
    objs = connection.iterable.order_by('score', 'name')
    assert objs.count() == 2
    assert objs[0].player == "bob"
    assert objs[1].player == "jen"


def test_filtering_embedded_fields(setup_data):
    filtering_opt = {
        "op": "OR",
        "filters": [
            {"info__continues__lt": 1},
        ],
    }

    field = FilteringConnectionField(HighScoreType)
    connection = field.default_resolver(None,
                                        {},
                                        filtering=filtering_opt)
    objs = connection.iterable.order_by('score', 'name')
    assert objs.count() == 2
    assert objs[0].player == "jim"
    assert objs[1].player == "jen"

    filtering_opt = {
        "op": "AND",
        "filters": [
            {"info__difficulty__icontains": "hard"},
            {"info__continues__lt": 1},
        ],
    }

    field = FilteringConnectionField(HighScoreType)
    connection = field.default_resolver(None,
                                        {},
                                        filtering=filtering_opt)
    objs = connection.iterable.order_by('score', 'name')
    assert objs.count() == 1
    assert objs[0].player == "jen"


# @TODO moved from test_custom_graphql
def test_filtering_connection_field_ordering(setup_data):
    client = graphene.test.Client(schema)
    res = client.execute('''{
        highscores (orderBy: "player") {
            edges {
                node {
                    id
                    player
                }
            }
        }
    }''')
    print(res)
    assert res['data']['highscores']['edges'][0]['node']['player'] == 'bob'
    assert res['data']['highscores']['edges'][7]['node']['player'] == 'zin'
