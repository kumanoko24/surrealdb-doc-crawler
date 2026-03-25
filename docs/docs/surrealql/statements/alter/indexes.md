---
title: ALTER INDEX statement
url: https://surrealdb.com/docs/surrealql/statements/alter/indexes
crawled_at: 2026-03-25 18:42:13
---

# ALTER INDEX statement


The `ALTER INDEX` statement is used to alter a defined index on a table.
SurrealQL SyntaxRailroad Diagram
SurrealQL Syntax

```
ALTER INDEX @name ON TABLE @table    COMMENT @string |    PREPARE REMOVE |    DROP COMMENT
```
ALTER INDEX@nameON TABLE@tableCOMMENT@stringPREPAREREMOVEDROPCOMMENT
## PREPARE REMOVE clause


As the name implies, an `ALTER INDEX PREPARE REMOVE` statement alters an index to prepare it for removal. This statement sets up a step in which the index has been decommissioned (prepared for removal), but not yet removed. At this point, `SELECT` queries along with the `EXPLAIN` clause to monitor query performance without the index.

```
-- 1. Decommission the indexALTER INDEX my_index ON my_table PREPARE REMOVE;-- 2. Monitor query performance and verify queries still workSELECT ... FROM my_table EXPLAIN;-- 3. If satisfied, permanently remove the indexREMOVE INDEX my_index ON my_table;
```

If removing the index is no longer desired, it can be restored to a useful state by using a REBUILD INDEX statement.

```
REBUILD INDEX my_index ON my_table;
```

## See also


- DEFINE INDEX
