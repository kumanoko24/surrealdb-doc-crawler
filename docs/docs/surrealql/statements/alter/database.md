---
title: ALTER DATABASE statement
url: https://surrealdb.com/docs/surrealql/statements/alter/database
crawled_at: 2026-03-25 18:42:10
---

# ALTER DATABASE statement


The `ALTER DATABASE` statement can be used to modify the database. `ALTER DATABASE` is used on the current database, which is why a `IF EXISTS` clause does not exist.

## Statement syntax

SurrealQL SyntaxRailroad Diagram
SurrealQL Syntax

```
ALTER DATABASE COMPACT
```
ALTER DATABASECOMPACT
## COMPACT


Performs storage compaction on the current database keyspace. To compact other resources, use ALTER SYSTEM to compact the entire datastore, ALTER NAMESPACE to compact the current namespace keyspace, or ALTER TABLE to compact a specific table keyspace.

The actual compaction used will depend on the datastore, such as RocksDB or SurrealKV.

This clause will not work with in-memory storage which has nothing persistent to compact, producing the following error:

```
'The storage layer does not support compaction requests.'
```

A successful compaction will return `NONE`.

```
ALTER DATABASE COMPACT;-- NONE
```

## See also


- DEFINE DATABASE
