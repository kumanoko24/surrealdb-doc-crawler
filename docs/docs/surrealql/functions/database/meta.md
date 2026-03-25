---
title: Meta functions
url: https://surrealdb.com/docs/surrealql/functions/database/meta
crawled_at: 2026-03-25 18:43:14
---

# Meta functions


###### Note


As of version 2.0, these functions are now part of SurrealDB's record functions.

These functions can be used to retrieve specific metadata from a SurrealDB Record ID.

| Function | Description |
| --- | --- |
| meta::id() | Extracts and returns the identifier from a SurrealDB Record ID |
| meta::tb() | Extracts and returns the table name from a SurrealDB Record ID |


## meta::id


The `meta::id` function extracts and returns the identifier from a SurrealDB Record ID.

API DEFINITION

```
meta::id(record) -> value
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN meta::id(person:tobie);"tobie"
```


## meta::tb


The `meta::tb` function extracts and returns the table name from a SurrealDB Record ID.

API DEFINITION

```
meta::tb(record) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN meta::tb(person:tobie);"person"
```

This function can also be called using the path `meta::table`.

```
RETURN meta::table(person:tobie);"person"
```
