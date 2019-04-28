This project is in a very early state. It achieves the core functionality below, but is missing niceties such as configuration options.

Better docs will come later. For now, please see the tests:
* [filtering tests](graphene_mongo_extras/filtering/tests)
* [other tests](graphene_mongo_extras/tests)

Check out [graphene-mongo-extras-examples](https://github.com/riverfr0zen/graphene-mongo-extras-examples) for a demo app and query examples.

# Overview
Provides some additional functionality on top of [graphene-mongo](https://github.com/graphql-python/graphene-mongo)
* Filtering
    - Filter using Mongoengine [query operators](http://docs.mongoengine.org/guide/querying.html#query-operators)
    - Provides the correct query operators in GraphQL for each field type
    - Nested filtering with AND/OR logic for filter sets
* total count in ConnectionField graphql queries (CountableConnectionBase)
* a way to set up interfaces (MongoengineInterface)
