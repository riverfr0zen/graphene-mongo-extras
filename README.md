This project is in a very early state. Documentation will come later. Please see the tests for examples.

Provides some additional functionality on top of [graphene-mongo](https://github.com/graphql-python/graphene-mongo)

* Filtering
    - Filter using Mongoengine [query operators](http://docs.mongoengine.org/guide/querying.html#query-operators)
    - Provides the correct query operators in GraphQL for each field type
    - Nested filtering with AND and OR logic
* total count in ConnectionField graphql queries (CountableConnectionBase)
* a way to set up interfaces (MongoengineInterface)
