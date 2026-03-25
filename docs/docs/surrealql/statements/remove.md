---
title: REMOVE statement
url: https://surrealdb.com/docs/surrealql/statements/remove
crawled_at: 2026-03-25 18:41:27
---

# REMOVE statement


The `REMOVE` statement is used to remove resources such as databases, tables, indexes, events and more.
Similar to an SQL DROP statement.

### Statement syntax

SurrealQL SyntaxRailroad Diagram
SurrealQL Syntax

```
REMOVE [    ACCESS    [ IF EXISTS ] @name ON [ NAMESPACE | DATABASE ]  | ANALYZER  [ IF EXISTS ] @name  | API       [ IF EXISTS ] @name  | DATABASE  [ IF EXISTS ] @name  | EVENT     [ IF EXISTS ] @name ON [ TABLE ] @table  | FIELD     [ IF EXISTS ] @name ON [ TABLE ] @table  | FUNCTION  [ IF EXISTS ] @name  | INDEX     [ IF EXISTS ] @name ON [ TABLE ] @table  | NAMESPACE [ IF EXISTS ] @name  | PARAM     [ IF EXISTS ] @name  | TABLE     [ IF EXISTS ] @name  | USER      [ IF EXISTS ] @name ON [ ROOT | NAMESPACE | DATABASE ]]
```
REMOVENAMESPACEIFEXISTS@nameDATABASEIFEXISTS@nameUSERIFEXISTS@nameONROOTNAMESPACEDATABASEACCESSIFEXISTS@nameONNAMESPACEDATABASEEVENTIFEXISTS@nameONTABLE@tableFIELDIFEXISTS@nameONTABLE@tableINDEXIFEXISTS@nameONTABLE@tableANALYZERIFEXISTS@nameFUNCTIONIFEXISTSfn::@namePARAMIFEXISTS$@nameTABLEIFEXISTS@name
## Example usage


### Basic usage


The following queries show an example of how to remove resources.

```
REMOVE NAMESPACE surrealdb;REMOVE DATABASE blog;REMOVE USER writer ON NAMESPACE;REMOVE USER writer ON DATABASE;REMOVE ACCESS token ON NAMESPACE;REMOVE ACCESS user ON DATABASE;REMOVE EVENT new_post ON TABLE article;-- Only works for Schemafull tables (i.e. tables with a schema)REMOVE FIELD tags ON TABLE article;REMOVE INDEX authors ON TABLE article;REMOVE ANALYZER example_ascii;REMOVE FUNCTION fn::update_author;REMOVE PARAM $author;REMOVE TABLE article;
```

### Using if exists clause


The following queries show an example of how to remove resources using the `IF EXISTS` clause, which will only remove the resource if it exists.

```
REMOVE NAMESPACE IF EXISTS surrealdb;REMOVE DATABASE IF EXISTS blog;REMOVE USER IF EXISTS writer ON NAMESPACE;REMOVE USER IF EXISTS writer ON DATABASE;REMOVE ACCESS IF EXISTS token ON NAMESPACE;REMOVE ACCESS IF EXISTS user ON DATABASE;REMOVE EVENT IF EXISTS new_post ON TABLE article;REMOVE FIELD IF EXISTS tags ON TABLE article;REMOVE INDEX IF EXISTS authors ON TABLE article;REMOVE ANALYZER IF EXISTS example_ascii;REMOVE FUNCTION IF EXISTS fn::update_author;REMOVE PARAM IF EXISTS $author;REMOVE TABLE IF EXISTS article;
```

### Usage in table views


A table used as a source for a table view cannot be removed until the table view itself has been removed.

```
DEFINE TABLE pc;DEFINE TABLE pc_agg AS SELECT count(), class FROM pc GROUP BY class;CREATE |pc:3| SET class = "Wizard";CREATE |pc:10| SET class = "Warrior";SELECT * FROM pc_agg;-- Error: pc_agg requires pc to workREMOVE TABLE pc;REMOVE TABLE pc_agg;-- pc_agg is now gone, pc can be removed tooREMOVE TABLE pc;
```

The `SELECT * FROM pc_agg` query shows that the table view is pulling data from the `pc` table. As long as the `pc` table exists, `pc_agg` cannot be removed.

```
-------- Query --------[  {     class: 'Warrior',     count: 10,     id: pc_agg:['Warrior']   },   {     class: 'Wizard',     count: 3,     id: pc_agg:['Wizard']   }]-------- Query --------'Invalid query: Cannot delete table `pc` on which a view is defined, table(s) `pc_agg` are defined as a view on this table.'
```

### Behaviour after removal


While all `REMOVE` statements remove the definition for a resource, some resources have additional actions when removed. They are:

- REMOVE DATABASE: This effectively deletes the database by removing the index stores, deleting the definition, and clearing the cache.
- REMOVE NAMESPACE: Same as REMOVE DATABASE, in addition to performing a remove on each database inside the namespace.
- REMOVE TABLE: Similar to the two previous statements but on a single table, and will fail if a table view depends on it. Removing a table will also send a KILL notification for each live query defined on it.
- REMOVE INDEX: This statement also removes the index store cache and index data. If you are considering removing an index but want to test the behaviour out first, use an ALTER INDEX PREPARE REMOVE statement. This will decommission the index, after which you can test out queries to see their behaviour as they would function after the index is removed. If acceptable then the index can then be removed, or the change can be reverted by rebuilding the index.

Another `REMOVE` statement to note is `REMOVE FIELD`, as it does not remove any existing data. To remove the existing data, perform an `UPDATE` or `UPSERT` statement that uses `UNSET` on the field or sets the field's value to `NONE`.

For a schemaless table, the existing data will remain present until unset.

```
DEFINE FIELD name ON person TYPE string;CREATE person:one SET name = "Billy";REMOVE FIELD name ON person;SELECT * FROM person; -- 'name' data is still thereUPDATE person; -- Does nothing-- [{ id: person:one, name: 'Billy' }]UPDATE person SET name = NONE; -- Must unset to remove 'name' data
```

For a schemafull table, read operations can be performed on a table that still contains data not defined in the schema. However, any updates will fail unless the field is unset to match the schema.

```
DEFINE TABLE person SCHEMAFULL;DEFINE FIELD name ON person TYPE string;CREATE person:one SET name = "Billy";REMOVE FIELD name ON person;SELECT * FROM person; -- 'name' data is still thereUPDATE person; -- Found field 'name', but no such field exists for table 'person'DEFINE FIELD created_at ON person TYPE datetime; -- Define a new field-- Works because values matche schema: 'name' is set to NONE, 'created_at' has a datetime valueUPDATE person SET name = NONE, created_at = time::now();
```
