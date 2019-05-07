import graphene
from graphene_mongo import MongoengineConnectionField
from mongoengine.queryset.visitor import Q
from graphql_relay.node.node import from_global_id
from graphene_mongo_extras.filtering import filterset_factory


class FilteringConnectionField(MongoengineConnectionField):
    def __init__(self, type, *args, **kwargs):
        kwargs.setdefault(
            'filtering',
            filterset_factory(type,
                              filtering_opts=type._meta.filtering)()
        )
        kwargs.setdefault('order_by', graphene.String())
        kwargs["get_queryset"] = self._get_queryset
        super(FilteringConnectionField, self).__init__(
            type,
            *args,
            **kwargs
        )
        # logger.debug(type._meta.fields["name"].__class__)

    def _build_q_args(self, finput):
        # logger.debug(finput)

        q_node = None
        # build args from "filters"
        op = finput["op"]
        if "filters" in finput:
            for fobj in finput['filters']:
                for query_op, compval in fobj.items():
                    condition = {query_op: compval}
                    if q_node is None:
                        q_node = Q(**condition)
                    elif op == "OR":
                        q_node = q_node.__or__(Q(**condition))
                    elif op == "AND":
                        q_node = q_node.__and__(Q(**condition))

        if "filtersets" in finput:
            for filterset in finput["filtersets"]:
                filterset_node = self._build_q_args(filterset)
                if q_node is None:
                    q_node = filterset_node
                elif op == "OR":
                    q_node = q_node.__or__(filterset_node)
                elif op == "AND":
                    q_node = q_node.__and__(filterset_node)

        return q_node

    def _get_queryset(self, model, info, **args):
        # logger.debug(type(info.context))
        filtering_input = args.pop('filtering', None)
        order_by = args.pop('order_by', None)

        q_args = None
        if filtering_input is not None:
            q_args = self._build_q_args(filtering_input)
        # logger.debug(q_args)
        if order_by:
            order_by = [f.strip() for f in order_by.split(',')]
            return model.objects.filter(q_args, **args).order_by(*order_by)
        return model.objects.filter(q_args, **args)

    def default_resolver(self, root, info, **args):
        pk = args.pop('id', None)
        if pk:
            args['pk'] = from_global_id(pk)[-1]
        return super().default_resolver(root, info, **args)
