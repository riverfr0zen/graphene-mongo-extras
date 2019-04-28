from graphene import List, Boolean, Int


def convert_for_lookup(field, lookup):
    if lookup in ['in', 'nin', 'all'] and field.__class__ is not List:
        return List(field.__class__)

    if lookup == 'exists':
        return Boolean()

    if lookup == 'mod':
        return List(Int)

    if lookup == 'size':
        return Int()

    return field
