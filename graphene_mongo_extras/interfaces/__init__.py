import graphene
from graphene.types.interface import InterfaceOptions
from graphene_mongo.types import construct_fields
from graphene.types.utils import yank_fields_from_attrs
from graphene_mongo.utils import is_valid_mongoengine_model
from graphene_mongo.registry import Registry, get_global_registry


class MongoengineInterfaceOptions(InterfaceOptions):
    model = None
    # filter_fields = ()
    only_fields = ()
    exclude_fields = ()


class MongoengineInterface(graphene.Interface):
    """
    Interface that derives fields from Mongoengine Document model.

    Much of this is adapted from graphene_mongo.types.MongoengineObjectType
    """

    @classmethod
    def __init_subclass_with_meta__(cls, _meta=None, model=None,
                                    only_fields=(), exclude_fields=(),
                                    # filter_fields=None,
                                    registry=None, **options):

        assert is_valid_mongoengine_model(model), (
            'The attribute model in {}.Meta must be a valid Mongoengine '
            'Model. Received "{}" instead.'
        ).format(cls.__name__, type(model))

        # Not adding to registry, since it only supports
        # MongoengineObjectType. Only using registry because required
        # by construct_fields
        if not registry:
            registry = get_global_registry()

        assert isinstance(registry, Registry), (
            'The attribute registry in {}.Meta needs to be an instance of '
            'Registry, received "{}".'
        ).format(cls.__name__, registry)

        converted_fields, self_referenced = construct_fields(
            model, registry, only_fields, exclude_fields
        )
        mongoengine_fields = yank_fields_from_attrs(converted_fields,
                                                    _as=graphene.Field)

        if not _meta:
            _meta = MongoengineInterfaceOptions(cls)
        _meta.model = model
        _meta.fields = mongoengine_fields
        _meta.only_fields = only_fields
        _meta.exclude_fields = exclude_fields
        # _meta.filter_fields = filter_fields

        super(MongoengineInterface, cls).__init_subclass_with_meta__(
            _meta=_meta,
            **options)
