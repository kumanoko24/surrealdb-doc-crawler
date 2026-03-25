---
title: ALTER TABLE statement
url: https://surrealdb.com/docs/surrealql/statements/alter/table
crawled_at: 2026-03-25 21:40:44
---

# ALTER TABLE statement


The `ALTER TABLE` statement is used to alter a defined table.
SurrealQL SyntaxRailroad Diagram
SurrealQL Syntax

```
ALTER TABLE [
	[ IF EXISTS ] @name
		[ DROP COMMENT ]
        [ DROP CHANGEFEED ]
        [ COMPACT ]
		[ SCHEMAFULL | SCHEMALESS ]
		[ PERMISSIONS [ NONE | FULL
			| FOR select @expression
			| FOR create @expression
			| FOR update @expression
			| FOR delete @expression
		] ]
    [ CHANGEFEED @duration ]
    [ COMMENT @string ] 
    [ CHANGEFEED ]
]

```

## COMPACT


Performs storage compaction on a specific table keyspace. To compact other resources, use [ALTER SYSTEM](/docs/surrealql/statements/alter/system) to compact the entire datastore, [ALTER NAMESPACE](/docs/surrealql/statements/alter/namespace) to compact the current namespace keyspace, or [ALTER DATABASE](/docs/surrealql/statements/alter/database) to compact the current database keyspace.

The actual compaction used will depend on the datastore, such as RocksDB or SurrealKV.

This clause will not work with in-memory storage which has nothing persistent to compact, producing the following error:

```
'The storage layer does not support compaction requests.'

```

A successful compaction will return `NONE`.

```
ALTER TABLE user COMPACT;
-- NONE

```

## See also


- DEFINE TABLE
