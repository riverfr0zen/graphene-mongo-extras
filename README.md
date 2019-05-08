This project is in a very early state. It achieves the core functionality below, but is missing niceties such as configuration options.

Better docs will come later. For now, please see the tests:
* [filtering tests](graphene_mongo_extras/filtering/tests)
* [other tests](graphene_mongo_extras/tests)

Check out [graphene-mongo-extras-examples](https://github.com/riverfr0zen/graphene-mongo-extras-examples) for a demo app and query examples.

# Overview / Todo-list

## Filtering Field
* [x] Filter using Mongoengine [query operators](http://docs.mongoengine.org/guide/querying.html#query-operators)
* [x] Provide the correct query operators in GraphQL for each field type
* [x] Nested filtering with AND/OR logic for filter sets
* [x] Ordering of results
* [x] Configure filtering field
    - [x] depth
    - [x] exclude fields
    - [ ] include fields
* [ ] Examine compatibility with various fields
* [ ] Support reference fields and list of reference fields

## Misc:
* [x] total count in ConnectionField graphql queries (CountableConnectionBase)
* [x] a way to set up interfaces (MongoengineInterface)

## Mutation support
* [ ] MongoengineInputObjectType
    - An InputObjectType that derives from an assigned model

## Embedded fields
* [ ] A way to implement embedded fields (and lists of) without having to use connections (i.e. return as SomeEmbeddedType or List[SomeEmbeddedType])

# Changelog

## 0.2.0
* MongoengineExtrasType added to support new Meta config options (in-lieu of MongoengineObjectType) 
* Filtering
    - Depth and excluded fields can now be configured


## 0.1.0
* Initial
