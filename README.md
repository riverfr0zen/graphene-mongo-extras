This project is in a very early state. It achieves the core functionality below, but is missing niceties such as configuration options.

Better docs will come later. For now, please see the tests:
* [filtering tests](graphene_mongo_extras/filtering/tests)
* [interfaces tests](graphene_mongo_extras/interfaces/tests)
* [other tests](graphene_mongo_extras/tests)

See the `examples` folder for a demo app and query examples.

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
* [x] Support list of embedded fields
* [ ] Examine compatibility with various fields
* [ ] Support reference fields and list of reference fields

## Interfaces
* [x] a way to set up interfaces (MongoNodeInterface)
* [x] use interfaces with list fields
* [x] use interfaces with connection fields
* See [example app](examples/example_ifaces_app.py)

## Misc:
* [x] total count in ConnectionField graphql queries (CountableConnectionBase)

## Mutation support
* [ ] MongoengineInputObjectType
    - An InputObjectType that derives from an assigned model


# Changelog

## 0.5.0
* MongoengineInterface now extends graphene.Node and renamed to MongoNodeInterface.
* Added [example app](examples/example_ifaces_app.py) showing the use of interfaces with list fields or connections.

## 0.4.0
* Filtering
    - Fixed required fields generating required filters ([issue 2](https://github.com/riverfr0zen/graphene-mongo-extras/issues/2))

## 0.3.0
* Filtering 
    - List of EmbeddedDocumentFields now supported [issue](https://github.com/riverfr0zen/graphene-mongo-extras/issues/1)
* Moved examples from separate repo into `examples` folder in this repo

## 0.2.0
* MongoengineExtrasType added to support new Meta config options (in-lieu of MongoengineObjectType) 
* Filtering
    - Depth and excluded fields can now be configured


## 0.1.0
* Initial
