---
title: ALTER SYSTEM statement
url: https://surrealdb.com/docs/surrealql/statements/alter/system
crawled_at: 2026-03-25 21:40:43
---

# ALTER SYSTEM statement


The `ALTER SYSTEM` statement is used to alter the entire datastore. It can be used to compact the system, or to set or drop a systemwide query timeout.

This statement is the only `ALTER` statement that does not have a corresponding `DEFINE` statement.

## Statement syntax

SurrealQL SyntaxRailroad Diagram
SurrealQL Syntax

```
ALTER SYSTEM 
    COMPACT |
    QUERY_TIMEOUT |
    DROP QUERY_TIMEOUT

```

## QUERY_TIMEOUT clause


A query timeout can be set for the system as a whole. The minimum possible timeout is one millisecond, below which the value will be set as `NONE`.

```
ALTER SYSTEM QUERY_TIMEOUT 100ns;
INFO FOR ROOT.config;

```

Output

```
{ QUERY_TIMEOUT: NONE }

```

Any value above `1ms` will set the timeout, beyond which no query that takes any longer than this will succeed.

```
ALTER SYSTEM QUERY_TIMEOUT 1ms;
FOR $_ IN 0..1000 {
    FOR $_ IN 0..1000 {
        CREATE |person:1000|;
    }
};

-- 'The query was not executed because it exceeded the timeout: 1ms'

```

## COMPACT clause


Compacts the entire datastore. To compact other resources, use [ALTER NAMESPACE](/docs/surrealql/statements/alter/namespace) to compact the current namespace keyspace, [ALTER DATABASE](/docs/surrealql/statements/alter/database) to compact the current database keyspace, or [ALTER TABLE](/docs/surrealql/statements/alter/table) to compact a specific table keyspace.

The actual compaction used will depend on the datastore, such as RocksDB or SurrealKV.

This clause will not work with in-memory storage which has nothing persistent to compact, producing the following error:

```
'The storage layer does not support compaction requests.'

```

A successful compaction will return `NONE`.

```
ALTER SYSTEM COMPACT;
-- NONE

```
