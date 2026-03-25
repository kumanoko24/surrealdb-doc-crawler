---
title: REBUILD statement
url: https://surrealdb.com/docs/surrealql/statements/rebuild
crawled_at: 2026-03-25 19:08:27
---

# `REBUILD` statement

The `REBUILD` statement is used to rebuild resources in SurrealDB. It is usually used in relation to a specified [Index to optimize performance. It is useful to rebuild indexes because sometimes [HNSW index performance can degrade due to frequent updates.

Rebuilding the index will ensure the index is fully optimized.

###### Note

Rebuilds are concurrent or sync based on how the index is defined. For example, if you define an index with the `CONCURRENTLY` option, the rebuild will be concurrent. Please see the [`CONCURRENTLY` clause section for more information.

### Statement syntax

SurrealQL Syntax

```REBUILD [
	INDEX [ IF EXISTS ] @name ON [ TABLE ] @table
]

```

###### Note

The `IF EXISTS` and TABLE clauses are optional.

## Example usage

For example, if you have a table called `book` and you have an index called `uniq_isbn` on the `isbn` field, you can rebuild the index using the following query:

```REBUILD INDEX uniq_isbn ON book;

```

### Using if exists clause

The following queries show an example of how to rebuild resources using the `IF EXISTS` clause, which will only rebuild the resource if it exists.

```REBUILD INDEX IF EXISTS uniq_isbn ON book;

```
