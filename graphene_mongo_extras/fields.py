from graphene import ConnectionField
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from graphene_mongo_extras.interfaces import MongoNodeInterface


class InterfaceConnectionField(MongoengineConnectionField):
    """ A subclass of MongoEngineConnectionField that supports
    implementing interfaces with the MongoNodeInterface class
    provided in this package. """

    @property
    def type(self):
        #
        # Overriding MongoengineConnectionField method to
        # support Interface connections with MongoNodeInterface
        #
        _type = super(ConnectionField, self).type
        assert (
            issubclass(_type, MongoengineObjectType) or
            issubclass(_type, MongoNodeInterface)
        ), ("InterfaceConnectionField only accepts MongoengineObjectType "
            "types or MongoNodeInterface subclasses")

        assert _type._meta.connection, (f"The type {_type.__name__} "
                                        "doesn't have a connection")
        return _type._meta.connection
