import graphene


def convert_for_lookup(field, lookup):
    if lookup in ['in', 'nin', 'all'] and field.__class__ is not graphene.List:
        return graphene.List(field.__class__)

    if lookup == 'exists':
        return graphene.Boolean()

    if lookup == 'mod':
        return graphene.List(graphene.Int)

    if lookup == 'size':
        return graphene.Int()

    return field
