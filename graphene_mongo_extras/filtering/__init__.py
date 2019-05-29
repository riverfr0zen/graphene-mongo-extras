import graphene
from copy import copy
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


def _is_embedded_list(field):
    if hasattr(field, 'field') and isinstance(
        field.field,
        EmbeddedDocumentField
    ):
        return True
    return False


def filters_factory(model, base_classname, filtering_opts={}, as_list=False):
    field_filters = {}
    graphene_mongo_registry = get_global_registry()
    filters_classname = "{}Filters".format(base_classname)
    filters_class = FiltersRegistry.get(filters_classname)
    if filters_class is None:
        for fieldname, orig_field in model._fields.items():
            field = copy(orig_field)
            field.required = False
            if 'exclude' in filtering_opts and \
                    fieldname in filtering_opts['exclude']:
                continue

            lookups = COMPARISON_OPERATORS
            if field.__class__ is StringField:
                lookups = lookups + STRING_OPERATORS
            lookups = filter(lambda l: l not in UNSUPPORTED_LOOKUPS,
                             lookups)

            if _is_embedded_list(field):
                filters = filters_factory(field.field.document_type,
                                          base_classname,
                                          as_list=True)
                filters = {"{}__{}".format(fieldname, filtr): fieldobj
                           for filtr, fieldobj in filters.items()}
                field_filters.update(filters)
            else:
                # @TODO: Review which cases using convert_mongoengine_field
                # may not be the most direct/efficient option (e.g. see the
                # "if" clause above)
                converted_field = convert_mongoengine_field(
                    field,
                    graphene_mongo_registry
                )
                if isinstance(converted_field, graphene.Dynamic):
                    # @TODO
                    # Currently only embedded fields supported, maybe
                    # in the future we can support reference fields if we
                    # provide additional filtering logic in fields.py to handle
                    # 'subqueries'
                    if isinstance(field, EmbeddedDocumentField):
                        filters = filters_factory(field.document_type,
                                                  base_classname,
                                                  as_list=True)
                        filters = {"{}__{}".format(fieldname, filtr): fieldobj
                                   for filtr, fieldobj in filters.items()}
                        field_filters.update(filters)
                else:
                    filters = [{
                        "{}__{}".format(fieldname, lookup):
                            convert_for_lookup(converted_field, lookup)
                    } for lookup in lookups]
                    field_filters.update(dict(ChainMap(*filters)))

        if as_list:
            return field_filters
        filters_class = type(filters_classname,
                             (graphene.InputObjectType,),
                             field_filters)
        FiltersRegistry.register(filters_class)
    return filters_class


def filterset_factory(gqltype, depth=None,
                      filtering_opts={}, filters_class=None,
                      filterset_class=None):
    model = gqltype._meta.model
    base_filterset_classname = gqltype.__name__
    if depth is None:
        if 'depth' in filtering_opts:
            depth = filtering_opts['depth']
        else:
            depth = DEFAULT_FILTERSET_DEPTH

    if not filters_class:
        filters_class = filters_factory(
            model,
            base_classname=base_filterset_classname,
            filtering_opts=filtering_opts,
        )

    depth_label = depth if depth > 0 else ''
    new_filterset_classname = "{}Filterset{}".format(base_filterset_classname,
                                                     depth_label)
    new_filterset_class = FiltersRegistry.get(new_filterset_classname)
    if not new_filterset_class:
        filterset_attrs = {"filters": graphene.List(filters_class)}
        if filterset_class:
            filterset_attrs["filtersets"] = graphene.List(filterset_class)

        new_filterset_class = type(new_filterset_classname,
                                   (FiltersetBase,),
                                   filterset_attrs)
        FiltersRegistry.register(new_filterset_class)

        if depth > 0:
            depth = depth - 1
            return filterset_factory(gqltype, depth=depth,
                                     filtering_opts=filtering_opts,
                                     filters_class=filters_class,
                                     filterset_class=new_filterset_class)
        # logger.debug(FiltersRegistry._registry.keys())
    return new_filterset_class
