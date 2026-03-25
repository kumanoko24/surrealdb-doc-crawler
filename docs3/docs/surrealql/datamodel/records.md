---
title: Record links
url: https://surrealdb.com/docs/surrealql/datamodel/records
crawled_at: 2026-03-25 21:40:29
---

# Record links


One of the most powerful features of SurrealDB is the ability to traverse from record-to-record without the need for traditional SQL JOINs. Each record ID points directly to a specific record in the database, without needing to run a table scan query. Record IDs can be stored within other records, allowing them to be linked together.

## Creating a record


When you create a record without specifying the id, then a randomly generated id is created and used for the record id.

```
CREATE person SET name = 'Tobie';

-- person:aio58g22n3upq16hsani

```

It's also possible to specify a specific record id when creating or updating records.

```
CREATE person:tester SET name = 'Tobie';

-- person:tester

```

## Select directly off of Record IDs


Because Record IDs are their own datatype in SurrealQL, you are able to select directly off of them.

```
CREATE person:tobie SET name = 'Tobie', email = 'tobie@surrealdb.com', opts.enabled = true;

-- Select the whole record
person:tobie.*;

-- Select specific fields
person:tobie.{ name, email };

```

## Storing record links within records


Records ids can be stored directly within other records, either as top-level properties, or nested within objects or arrays.

```
CREATE person:jaime SET name = 'Jaime', friends = [person:tobie, person:simon];
CREATE person:tobie SET name = 'Tobie', friends = [person:simon, person:marcus];
CREATE person:simon SET name = 'Simon', friends = [person:jaime, person:tobie];
CREATE person:marcus SET name = 'Marcus', friends = [person:tobie];

```

## Fetching remote records from within records


Nested field traversal can be used to fetch the properties from the remote records, as if the record was embedded within the record being queried.

```
SELECT friends.name FROM person:tobie;
[
	{
		friends: {
			name: ["Simon", "Marcus"]
		}
	}
]

```

There is no limit to the number of remote traversals that can be performed in a query. Using `.` dot notation, SurrealDB does not differentiate between nested object properties, or remote records, and will fetch remote records asynchronously when needed for a query.

```
SELECT friends.friends.friends.name FROM person:tobie;
[
	{
		friends: {
			friends: {
				friends: {
					name: [
						[ ["Tobie", "Simon"], ["Simon", "Marcus"] ],
						[ ["Simon", "Marcus"] ]
					]
				}
			}
		}
	}
]

```

## Next steps


You've now seen how to create records using randomly generated ids, or specific record ids. This is just the beginning! The power and flexibility which is possible with the remote record fetching functionality within queries opens up a whole new set of possibilities for storing and querying traditional data, and connected datasets. The next page follows up with a feature available in SurrealDB since version 2.2.0: the ability to use record links in a bidirectional manner thanks to reference tracking.

Also check out this explainer video on using record links in SurrealDB:
