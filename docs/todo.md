# Filtering Field
* [x] Filter using Mongoengine [query operators](http://docs.mongoengine.org/guide/querying.html#query-operators)
* [x] Provide the correct query operators in GraphQL for each field type
* [x] Nested filtering with AND/OR logic for filter sets
* [x] Ordering of results
* [x] Configure filtering field
    - [x] depth
    - [x] include/exclude fields
* [ ] Examine compatibility with various fields
* [ ] Support reference fields and list of reference fields

# Mutation support
* [ ] MongoengineInputObjectType
    - An InputObjectType that derives from an assigned model

# Embedded fields
[ ] A way to implement embedded fields (and lists of) without having to use connections (i.e. return as SomeEmbeddedType or List[SomeEmbeddedType])
