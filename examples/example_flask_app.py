import graphene
from flask import Flask
from flask_graphql import GraphQLView
from datetime import datetime
from mongoengine import connect
from graphene_mongo_extras.filtering.fields import FilteringConnectionField
from graphene_mongo_extras.filtering.tests.models import HighScore, \
                                                         PlaythruInfo, \
                                                         Game
from graphene_mongo_extras.filtering.tests import types

connect(host='mongomock://localhost', db='graphene-mongo-extras')


class Query(graphene.ObjectType):
    games = FilteringConnectionField(types.GameType)
    games2 = FilteringConnectionField(types.GameType2)
    highscores = FilteringConnectionField(types.HighScoreType)


schema = graphene.Schema(
    query=Query,
    types=[
        types.GameType,
        types.GameType2,
        types.HighScoreType,
        # types.PlaythruInfoType
    ]
)

#
# Setup data
#
Game.drop_collection()
HighScore.drop_collection()
HighScore(player="liz", score=5, recorded=datetime(2019, 1, 1),
          info=PlaythruInfo(difficulty="easy", continues=2)).save(),
HighScore(player="bob", score=1, recorded=datetime(2019, 1, 1),
          cheats=['No damage'],
          info=PlaythruInfo(difficulty="easy", continues=3)).save(),
HighScore(player="boo", score=5, recorded=datetime(2019, 1, 2),
          info=PlaythruInfo(difficulty="medium", continues=1)).save(),
HighScore(player="jim", score=7, recorded=datetime(2019, 1, 3),
          info=PlaythruInfo(difficulty="medium", continues=0)).save(),

HighScore(player="zin", score=8, recorded=datetime(2019, 1, 3),
          cheats=['99 lives'],
          info=PlaythruInfo(difficulty="hard", continues=2)).save(),
HighScore(player="jen", score=10, recorded=datetime(2019, 1, 3),
          info=PlaythruInfo(difficulty="hard", continues=0)).save(),
HighScore(player="dav", score=10, recorded=datetime(2019, 1, 5),
          info=PlaythruInfo(difficulty="hard", continues=1)).save(),
HighScore(player="sam", score=1, recorded=datetime(2019, 1, 5),
          cheats=['No damage', '99 lives'],
          info=PlaythruInfo(difficulty="medium", continues=1)).save(),

Game(name='Space Invaders', publisher='Taito',
     desc="The original",
     scores=[
        HighScore.objects.get(player='liz'),
        HighScore.objects.get(player='bob'),
        HighScore.objects.get(player='boo'),
        HighScore.objects.get(player='jim'),
     ],
     options=[
        PlaythruInfo(difficulty="very easy", continues=100),
        PlaythruInfo(difficulty="easy", continues=30),
        PlaythruInfo(difficulty="normal", continues=10),
        PlaythruInfo(difficulty="hard", continues=5),
        PlaythruInfo(difficulty="pain", continues=0),
     ]).save(),
Game(name='Space Invaders 2', publisher='Taito',
     scores=[
        HighScore.objects.get(player='zin'),
        HighScore.objects.get(player='jen'),
        HighScore.objects.get(player='dav'),
        HighScore.objects.get(player='sam'),
     ],
     options=[
        PlaythruInfo(difficulty="relaxed", continues=50),
        PlaythruInfo(difficulty="intense", continues=1),
     ],
     alt_options=[
        PlaythruInfo(difficulty="why bother", continues=999),
        PlaythruInfo(difficulty="mystery", continues=5),
     ]).save(),


app = Flask(__name__)
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql',
                                  schema=schema,
                                  graphiql=True))
