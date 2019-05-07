import graphene
from graphene_mongo.converter import convert_mongoengine_field
from graphene_mongo.registry import get_global_registry
from collections import ChainMap
from mongoengine.fields import StringField, EmbeddedDocumentField
from mongoengine.queryset.transform import COMPARISON_OPERATORS, \
                                           STRING_OPERATORS
from .utils import convert_for_lookup

DEFAULT_FILTERSET_DEPTH = 2
UNSUPPORTED_LOOKUPS = ('type', 'not', 'match', 'elemMatch')


class FiltersRegistry:
    _registry = {}

    @classmethod
    def register(cls, filterset_class):
        cls._registry[filterset_class.__name__] = filterset_class

    @classmethod
    def get(cls, classname):
        if classname in cls._registry:
            return cls._registry[classname]
        return None


class FiltersetBase(graphene.InputObjectType):
    op = graphene.String(default_value="AND")


def filters_factory(model, filtering_opts={}, as_list=False):
    field_filters = {}
    graphene_mongo_registry = get_global_registry()
    filters_classname = "{}Filters".format(model.__name__)
    filters_class = FiltersRegistry.get(filters_classname)
    if filters_class is None:
        for fieldname, field in model._fields.items():
            lookups = COMPARISON_OPERATORS
            # logger.debug(field.__class__)
            if field.__class__ is StringField:
                lookups = lookups + STRING_OPERATORS
            lookups = filter(lambda l: l not in UNSUPPORTED_LOOKUPS,
                             lookups)
            converted_field = convert_mongoengine_field(
                field,
                graphene_mongo_registry
            )
            if not isinstance(converted_field, graphene.Dynamic):
                filters = [{
                    "{}__{}".format(fieldname, lookup):
                        convert_for_lookup(converted_field, lookup)
                } for lookup in lookups]
                field_filters.update(dict(ChainMap(*filters)))
            else:
                # @TODO
                # Currently only embedded fields supported, maybe
                # in the future we can support reference fields if we
                # provide additional filtering logic in fields.py to handle
                # 'subqueries'
                if isinstance(field, EmbeddedDocumentField):
                    filters = filters_factory(field.document_type,
                                              as_list=True)
                    filters = {"{}__{}".format(fieldname, filtr): fieldobj
                               for filtr, fieldobj in filters.items()}
                    field_filters.update(filters)
                    # logger.debug(filters.keys())
        if as_list:
            return field_filters
        filters_class = type(filters_classname,
                             (graphene.InputObjectType,),
                             field_filters)
        FiltersRegistry.register(filters_class)
        return filters_class


def filterset_factory(model, depth=DEFAULT_FILTERSET_DEPTH,
                      filtering_opts={}, filters_class=None,
                      filterset_class=None):
    if 'depth' in filtering_opts:
        depth = filtering_opts['depth']

    # logger.debug([field for fieldname, field in model._fields.items()])
    if not filters_class:
        filters_class = filters_factory(model)

    depth_label = depth if depth > 0 else ''
    new_filterset_classname = "{}Filterset{}".format(model.__name__,
                                                     depth_label)
    filterset_attrs = {"filters": graphene.List(filters_class)}
    if filterset_class:
        filterset_attrs["filtersets"] = graphene.List(filterset_class)

    new_filterset_class = type(new_filterset_classname,
                               (FiltersetBase,),
                               filterset_attrs)
    FiltersRegistry.register(new_filterset_class)

    if depth > 0:
        depth = depth - 1
        return filterset_factory(model, depth=depth,
                                 filtering_opts=filtering_opts,
                                 filters_class=filters_class,
                                 filterset_class=new_filterset_class)
    # logger.debug(FiltersRegistry._registry.keys())
    return new_filterset_class
