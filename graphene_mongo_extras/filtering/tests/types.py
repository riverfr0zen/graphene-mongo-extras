from graphene.relay import Node
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from graphene_mongo_extras import MongoengineExtrasType
from ..fields import FilteringConnectionField
from .models import HighScore, Game, PlaythruInfo


class HighScoreType(MongoengineObjectType):
    class Meta:
        model = HighScore
        interfaces = (Node,)
        connection_field_class = MongoengineConnectionField


class PlaythruInfoType(MongoengineObjectType):
    class Meta:
        model = PlaythruInfo
        interfaces = (Node,)
        connection_field_class = MongoengineConnectionField


class GameType(MongoengineExtrasType):
    class Meta:
        model = Game
        interfaces = (Node,)
        exclude_fields = ('description',)
        # filtering = {'depth': 3, 'exclude': ['scores', 'options']}
        filtering = {'depth': 3, 'exclude': ['scores']}
        connection_field_class = FilteringConnectionField


class GameType2(MongoengineExtrasType):
    """ A type to test alternate configuration """
    class Meta:
        model = Game
        interfaces = (Node,)
        exclude_fields = ('scores', 'description')
        connection_field_class = FilteringConnectionField
