---
title: UPDATE statement
url: https://surrealdb.com/docs/surrealql/statements/update
crawled_at: 2026-03-25 18:41:36
---

# UPDATE statement


The `UPDATE` statement can be used to update existing records in the database. If the record does not exist, the statement will succeed but no records will be updated.

###### Note


This statement can not be used to create graph relationships. For that, use the RELATE or INSERT statement.

###### Note


UPDATE on a single record in SurrealDB 1.x will create the record if it does not exist. This behaviour is no longer the case in SurrealDB 2.0. To update and create a record if it does not exist in SurrealDB 2.0, use the UPSERT statement.

### Statement syntax

SurrealQL SyntaxRailroad Diagram
SurrealQL Syntax

```
UPDATE [ ONLY ] @targets	[ CONTENT @value	  | MERGE @value	  | PATCH @value	  | REPLACE @value	  | [ SET @field = @value, ... | UNSET @field, ... ]	]	[ WHERE @condition ]	[ RETURN NONE | RETURN BEFORE | RETURN AFTER | RETURN DIFF | RETURN @statement_param, ... | RETURN VALUE @statement_param ]	[ TIMEOUT @duration ]	[ EXPLAIN [ FULL ]];
```
UPDATEONLY@targetsCONTENT@valueMERGE@valuePATCH@valueREPLACE@valueSETUNSET@field (=|,) @value ...WHERE@conditionRETURNNONEBEFOREAFTERDIFF@statement_param, ...VALUE@statement_paramTIMEOUT@durationEXPLAINFULL;
###### Note


`@target` refers to either record output including an `id` field, or a record ID on its own.

## Example usage


Let's look at some examples of how to use the `UPDATE` statement. First we'll create two `person` records with the CREATE statement so that the examples will produce a meaningful output.

```
-- Create a Schemaless person table with a random idCREATE person CONTENT {    name: 'John',    company: 'Surrealist',    skills: ['JavaScript', 'Go' , 'SurrealQL']};-- Create another person with a specific idCREATE person:tobie CONTENT {    name: 'Tobie',    company: 'SurrealDB',    skills: ['JavaScript', 'Go' , 'SurrealQL']};
```

Let's say we wanted to update the `person` table with a new field `enjoys` (an array), a new skill `breathing` to the existing `skills` field (another array), add a new numeric field called `dollars`, and a `last_name` field that relies on the existing `name` field to set its value.

To do this we would use the following query.

```
-- Update all records in a table-- The `enjoys` field will also be an array.-- The += operator alone is enough to infer the typeUPDATE person SET 	dollars = 50,	skills += 'breathing',	enjoys += 'reading',	full_name = name + ' Mc' + name + 'erson';
```

Output

```
[	{		company: 'Surrealist',		dollars: 50,		enjoys: [			'reading'		],		full_name: 'John McJohnerson',		id: person:j1qov2pxey3p8s6hqlev,		name: 'John',		skills: [			'JavaScript',			'Go',			'SurrealQL',			'breathing'		]	},	{		company: 'SurrealDB',		dollars: 50,		enjoys: [			'reading'		],		full_name: 'Tobie McTobieerson',		id: person:tobie,		name: 'Tobie',		skills: [			'JavaScript',			'Go',			'SurrealQL',			'breathing'		]	}]
```

For more specific updates, you can specify a record ID to update a single record. The following query will update the record with the ID `person:tobie` to add "Rust" as a skill.

```
-- Update a record with a specific string id to add a new skill: 'Rust'UPDATE person:tobie SET skills += 'Rust';
```

Output

```
[	{		company: 'SurrealDB',		dollars: 50,		enjoys: [			'reading'		],		full_name: 'Tobie McTobieerson',		id: person:tobie,		name: 'Tobie',		skills: [			'JavaScript',			'Go',			'SurrealQL',			'breathing',			'Rust'		]	}]
```

The `-=` operator can be used to remove an item from an array or reduce a numeric value by a certain value.

```
UPDATE person:tobie SET 	skills -= 'Go', 	dollars -= 1;
```

Output

```
[	{		company: 'SurrealDB',		dollars: 49,		enjoys: [			'reading'		],		full_name: 'Tobie McTobieerson',		id: person:tobie,		name: 'Tobie',		skills: [			'JavaScript',			'SurrealQL',			'breathing',			'Rust'		]	}]
```

You can also remove a field from a record using the `UNSET` keyword or by setting the field to `NONE`.

```
-- Remove the company field by setting it to NONE or using the UNSET keywordUPDATE person:tobie SET company = NONE;UPDATE person:tobie UNSET company;
```

Output

```
[	{		dollars: 49,		enjoys: [			'reading'		],		full_name: 'Tobie McTobieerson',		id: person:tobie,		name: 'Tobie',		skills: [			'JavaScript',			'SurrealQL',			'breathing',			'Rust'		]	}]
```

## Conditional Update with WHERE clause


The `UPDATE` statement supports conditional matching of records using a `WHERE` clause. If the expression in the `WHERE` clause evaluates to `true`, then the respective record will be updated.

```
-- Update all records which match the condition that `company` is not equal to "SurrealDB"UPDATE person SET skills += "System design" WHERE company != "SurrealDB";
```

Output

```
[	{		company: 'Surrealist',		dollars: 50,		enjoys: [			'reading'		],		full_name: 'John McJohnerson',		id: person:i5z3i64cpqpo8jtr6jww,		name: 'John',		skills: [			'JavaScript',			'Go',			'SurrealQL',			'breathing',			'System design'		]	},	{		dollars: 49,		enjoys: [			'reading'		],		full_name: 'Tobie McTobieerson',		id: person:tobie,		name: 'Tobie',		skills: [			'JavaScript',			'SurrealQL',			'breathing',			'Rust',			'System design'		]	}]
```

## CONTENT clause


Instead of specifying record data using the `SET` clause, it is also possible to use the `CONTENT` keyword to specify the record data using a SurrealQL object.

```
-- Update all records with the same contentUPDATE person CONTENT {	name: 'John',	company: 'SurrealDB',	skills: ['Rust', 'Go', 'JavaScript'],};-- Oops, now they are both named John.-- Update a specific record with some contentUPDATE person:tobie CONTENT {	name: 'Tobie',	company: 'SurrealDB',	skills: ['Rust', 'Go', 'JavaScript'],};
```

Since version `2.1.0`, a statement with a `CONTENT` clause will bypass `READONLY` fields instead of generating an error.

```
DEFINE FIELD created ON person TYPE datetime DEFAULT d'2024-01-01T00:00:00Z' READONLY;CREATE person:gladys SET age = 90;-- Does not try to modify `created` field, no errorUPDATE person:gladys CONTENT { age: 70 };
```
Output before 2.1.0Output after 2.1.0
```
-------- Query --------[	{		age: 90,		created: d'2024-01-01T00:00:00Z',		id: person:gladys	}]-------- Query --------'Found changed value for field `created`, with record `person:gladys`, but field is readonly'
```

```
-------- Query --------[	{		age: 90,		created: d'2024-01-01T00:00:00Z',		id: person:gladys	}]-------- Query --------[	{		age: 70,		created: d'2024-01-01T00:00:00Z',		id: person:gladys	}]
```

## REPLACE clause


Originally an alias for `CONTENT`, the `REPLACE` clause maintains the previous behaviour regarding `READONLY` fields. If the content following `REPLACE` does not match a record's `READONLY` fields, an error will be generated.

```
DEFINE FIELD created ON person TYPE datetime DEFAULT d'2024-01-01T00:00:00Z' READONLY;CREATE person:gladys SET age = 90;-- Attempts to change `created` field, errorUPDATE person:gladys REPLACE { age: 70 };-- `created` equals current value, query worksUPDATE person:gladys REPLACE { age: 70, created: d'2024-01-01T00:00:00Z' };
```

Output

```
-------- Query --------[	{		age: 90,		created: d'2024-01-01T00:00:00Z',		id: person:gladys	}]-------- Query --------'Found changed value for field `created`, with record `person:gladys`, but field is readonly'-------- Query --------[	{		age: 70,		created: d'2024-01-01T00:00:00Z',		id: person:gladys	}]
```

## MERGE clause


Instead of specifying the full record data using `CONTENT` or one field at a time using `SET`, it is also possible to merge-update only specific fields by using the `MERGE` keyword followed by on object containing the fields which are to be upserted.

```
-- Update certain fields on all recordsUPDATE person MERGE {	settings: {		marketing: true,	},};-- Update certain fields on a specific recordUPDATE person:tobie MERGE {	settings: {		marketing: true,	},};
```

Output

```
[	{		company: 'SurrealDB',		id: person:i5z3i64cpqpo8jtr6jww,		name: 'John',		settings: {			marketing: true		},		skills: [			'Rust',			'Go',			'JavaScript'		]	},	{		company: 'SurrealDB',		id: person:tobie,		name: 'Tobie',		settings: {			marketing: true		},		skills: [			'Rust',			'Go',			'JavaScript'		]	}]
```

## PATCH clause


You can also specify changes to be applied to your query response, using the PATCH command which works similar to the JSON Patch specification

```
-- Patch the JSON responseUPDATE person:tobie PATCH [	{		"op": "add",		"path": "Engineering",		"value": "true"	}]
```

Output

```
[	{		Engineering: 'true',		company: 'SurrealDB',		id: person:tobie,		name: 'Tobie',		settings: {			marketing: true		},		skills: [			'Rust',			'Go',			'JavaScript'		]	}]
```

## Alter the RETURN value


By default, the update statement returns the record value once the changes have been made. To change the return value of each record, use the `RETURN` clause, specifying `NONE`, `BEFORE`, `AFTER`, `DIFF`, a comma-separated list of specific fields or ad-hoc fields, or `VALUE` for a single field without its key name.

```
-- Don't return any resultUPDATE person SET skills += 'reading' RETURN NONE;-- Return the changeset diffUPDATE person SET skills += 'reading' RETURN DIFF;-- Return the record before changes were appliedUPDATE person SET skills += 'reading' RETURN BEFORE;-- Return the record after changes were applied (the default)UPDATE person SET skills += 'reading' RETURN AFTER;-- Return the value of the 'skills' field without the field nameUPDATE person SET skills += 'reading' RETURN VALUE skills;-- Return a specific field only from the updated recordsUPDATE person:tobie SET skills = ['skiing', 'music'] RETURN name, interests;
```

## Using a timeout


When processing a large result set with many interconnected records, it is possible to use the `TIMEOUT` keyword to specify a timeout duration for the statement. If the statement continues beyond this duration, then the transaction will fail, no records will be updated in the database, and the statement will return an error.

```
UPDATE person 	SET important = true 	WHERE ->knows->person->(knows WHERE influencer = true) 	TIMEOUT 5s;
```

## UPDATE inside database exports


As `UPDATE` before version 2.0.0 used to create a specified record ID if it did not exist, it was used in the `.surql` files generated by the surreal export command to export existing records in a database. As of version 2.0.0, the INSERT statement is used instead.

## The EXPLAIN clause


When `EXPLAIN` is used:

1. The UPDATE statement returns an explanation, essentially revealing the execution plan to provide transparency and understanding of the query performance.
2. The records are not updated.

`EXPLAIN` can be followed by `FULL` to see the number of executed rows.
