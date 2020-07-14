import graphene
from graphene_mongo.types import MongoengineObjectType, \
                                 MongoengineObjectTypeOptions
from graphene.relay import Connection
from .fields import InterfaceConnectionField
from .filtering.fields import FilteringConnectionField
from .interfaces import MongoNodeInterface

__version__ = '0.7.0'

__all__ = [
    'MongoengineExtrasType',
    'CountableConnectionBase',
    'InterfaceConnectionField',
    'FilteringConnectionField',
    'MongoNodeInterface',
]


class MongoengineExtrasType(MongoengineObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, filtering={}, _meta=None, **kwargs):
        if not _meta:
            _meta = MongoengineObjectTypeOptions(cls)
            _meta.filtering = filtering
        super(MongoengineExtrasType, cls) \
            .__init_subclass_with_meta__(_meta=_meta, **kwargs)


class CountableConnectionBase(Connection):
    """ Based on:
    https://github.com/graphql-python/graphene-django/issues/162#issuecomment-347639067
    """
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info, **kwargs):
        return self.list_length
