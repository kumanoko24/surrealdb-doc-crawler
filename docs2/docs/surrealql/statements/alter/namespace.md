---
title: ALTER NAMESPACE statement
url: https://surrealdb.com/docs/surrealql/statements/alter/namespace
crawled_at: 2026-03-25 19:10:41
---

# `ALTER NAMESPACE` statement

The `ALTER NAMESPACE` statement can be used to modify the namespace. `ALTER NAMESPACE` is used on the current namespace, which is why a `IF EXISTS` clause does not exist.

## Statement syntax

SurrealQL Syntax

```ALTER NAMESPACE COMPACT

```

## COMPACT

Performs storage compaction onPerforms storage compaction on the current namespace keyspace. To compact other resources, use [ALTER SYSTEM to compact the entire datastore, [ALTER DATABASE to compact the current database keyspace, or [ALTER TABLE to compact a specific table keyspace.

The actual compaction used will depend on the datastore, such as RocksDB or SurrealKV.

This clause will not work with in-memory storage which has nothing persistent to compact, producing the following error:

```'The storage layer does not support compaction requests.'

```

A successful compaction will return `NONE`.

```ALTER NAMESPACE COMPACT;
-- NONE

```

## See also

- 
[`DEFINE NAMESPACE`
