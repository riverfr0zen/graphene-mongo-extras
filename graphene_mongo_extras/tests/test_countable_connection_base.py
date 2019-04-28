import graphene
from graphene.test import Client
from mongoengine import Document
from mongoengine.fields import StringField
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from graphene_mongo_extras import CountableConnectionBase


class Smooch(Document):
    rating = StringField()


class SmoochType(MongoengineObjectType):
    class Meta:
        model = Smooch
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnectionBase
        connection_field_class = MongoengineConnectionField


class Query(graphene.ObjectType):
    smooches = MongoengineConnectionField(SmoochType)


schema = graphene.Schema(
    query=Query,
    types=[SmoochType, ]
)


def test_countable_connection_base(setup_mongo):
    for i in range(10):
        Smooch(rating=str(i)).save()

    client = Client(schema)
    res = client.execute('''{
        smooches {
            totalCount
            edges {
                node {
                    id
                }
            }
        }
    }''')
    assert res['data']['smooches']['totalCount'] == 10
    Smooch.drop_collection()
