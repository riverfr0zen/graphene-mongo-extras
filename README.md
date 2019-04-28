This project is in a very early state. It achieves most of the functionality below, but very minimally at the moment. 

Better docs will come later. For now, please see the tests for examples. Test are at:
* [filtering tests](graphene_mongo_extras/filtering/tests)
* [other tests](graphene_mongo_extras/tests)


# Overview
Provides some additional functionality on top of [graphene-mongo](https://github.com/graphql-python/graphene-mongo)
* Filtering
    - Filter using Mongoengine [query operators](http://docs.mongoengine.org/guide/querying.html#query-operators)
    - Provides the correct query operators in GraphQL for each field type
    - Nested filtering with AND/OR logic for filter sets
* total count in ConnectionField graphql queries (CountableConnectionBase)
* a way to set up interfaces (MongoengineInterface)
