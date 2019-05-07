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


class HighScoreWithOptionsType(MongoengineExtrasType):
    class Meta:
        model = HighScore
        interfaces = (Node,)
        filtering = {'depth': 3}
        connection_field_class = FilteringConnectionField


class Query(graphene.ObjectType):
    highscores = FilteringConnectionField(HighScoreType)
    hs_with_options = FilteringConnectionField(HighScoreWithOptionsType)


schema = graphene.Schema(
    query=Query,
    types=[
        HighScoreType,
    ]
)


def test_filterset_depth():
    # HighScoreType has default depth of 2
    hs_filters = FiltersRegistry.get('HighScoreTypeFilters')
    assert hs_filters

    hs_filterset = FiltersRegistry.get('HighScoreTypeFilterset')
    assert hs_filterset
    assert hasattr(hs_filterset, 'filters')
    assert hs_filterset.filters.of_type().__class__.__name__ \
        == 'HighScoreTypeFilters'
    assert hasattr(hs_filterset, 'filtersets')
    assert hs_filterset.filtersets.of_type().__class__.__name__ \
        == 'HighScoreTypeFilterset1'

    # hs_filters_class = hs_filterset.filters.of_type()
    # assert isinstance(hs_filterset.filters, hs_filters_class)

    hs_filterset1 = FiltersRegistry.get('HighScoreTypeFilterset1')
    assert hs_filterset1
    assert hasattr(hs_filterset1, 'filters')
    assert hs_filterset1.filters.of_type().__class__.__name__ \
        == 'HighScoreTypeFilters'
    assert hasattr(hs_filterset1, 'filtersets')
    assert hs_filterset1.filtersets.of_type().__class__.__name__ \
        == 'HighScoreTypeFilterset2'

    hs_filterset2 = FiltersRegistry.get('HighScoreTypeFilterset2')
    assert hs_filterset2
    assert hasattr(hs_filterset2, 'filters')
    assert hs_filterset2.filters.of_type().__class__.__name__ \
        == 'HighScoreTypeFilters'
    assert not hasattr(hs_filterset2, 'filtersets')

    hs_filterset3 = FiltersRegistry.get('HighScoreTypeFilterset3')
    assert not hs_filterset3

    # HighScoreWithOptionsType has depth of 3
    hso_filters = FiltersRegistry.get('HighScoreWithOptionsTypeFilters')
    assert hso_filters

    hso_filterset = FiltersRegistry.get('HighScoreWithOptionsTypeFilterset')
    assert hso_filterset
    assert hasattr(hso_filterset, 'filters')
    assert hso_filterset.filters.of_type().__class__.__name__ \
        == 'HighScoreWithOptionsTypeFilters'
    assert hasattr(hso_filterset, 'filtersets')
    assert hso_filterset.filtersets.of_type().__class__.__name__ \
        == 'HighScoreWithOptionsTypeFilterset1'

    hso_filterset1 = FiltersRegistry.get('HighScoreWithOptionsTypeFilterset1')
    assert hso_filterset1
    assert hasattr(hso_filterset1, 'filters')
    assert hso_filterset1.filters.of_type().__class__.__name__ \
        == 'HighScoreWithOptionsTypeFilters'
    assert hasattr(hso_filterset1, 'filtersets')
    assert hso_filterset1.filtersets.of_type().__class__.__name__ \
        == 'HighScoreWithOptionsTypeFilterset2'

    hso_filterset2 = FiltersRegistry.get('HighScoreWithOptionsTypeFilterset2')
    assert hso_filterset2
    assert hasattr(hso_filterset1, 'filters')
    assert hso_filterset2.filters.of_type().__class__.__name__ \
        == 'HighScoreWithOptionsTypeFilters'
    assert hasattr(hso_filterset2, 'filtersets')
    assert hso_filterset2.filtersets.of_type().__class__.__name__ \
        == 'HighScoreWithOptionsTypeFilterset3'

    hso_filterset3 = FiltersRegistry.get('HighScoreWithOptionsTypeFilterset3')
    assert hso_filterset3
    assert hasattr(hso_filterset3, 'filters')
    assert not hasattr(hs_filterset3, 'filtersets')

    hso_filterset4 = FiltersRegistry.get('HighScoreWithOptionsTypeFilterset4')
    assert not hso_filterset4


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
