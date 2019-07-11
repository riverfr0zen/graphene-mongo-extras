from mongoengine import Document, fields
from bson import ObjectId
from graphene_mongo_extras.tests.conftest import setup_mongo


class Packaging(Document):
    name = fields.StringField()


class Toy(Document):
    meta = {'allow_inheritance': True}

    id = fields.ObjectIdField(primary_key=True, default=ObjectId)
    name = fields.StringField()
    packaging = fields.ReferenceField(Packaging)


class Plushie(Toy):
    animal = fields.StringField()


class Videogame(Toy):
    genre = fields.StringField()
