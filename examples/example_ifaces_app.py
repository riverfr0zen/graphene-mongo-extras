from flask import Flask
from flask_graphql import GraphQLView
from mongoengine import connect
from graphene_mongo_extras.interfaces.tests.schema import schema
from graphene_mongo_extras.interfaces.tests.models import Packaging, \
                                                          Plushie, Videogame


connect(host='mongomock://localhost', db='graphene-mongo-extras')

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


app = Flask(__name__)
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql',
                                  schema=schema,
                                  graphiql=True))
