from mongoengine import Document, fields
from graphene_mongo_extras import MongoengineExtrasType


class SomeModel(Document):
    somefield = fields.StringField()


class SomeExtrasType(MongoengineExtrasType):
    class Meta:
        model = SomeModel
        filtering = {'depth': 2}


def test_meta_options():
    assert hasattr(SomeExtrasType._meta, 'filtering')
    assert 'depth' in SomeExtrasType._meta.filtering
    assert SomeExtrasType._meta.filtering['depth'] == 2
