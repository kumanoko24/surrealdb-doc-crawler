---
title: Record functions
url: https://surrealdb.com/docs/surrealql/functions/database/record
crawled_at: 2026-03-25 21:42:37
---

# Record functions


###### Note


Record functions before SurrealDB 2.0 were located inside the module [meta](/docs/surrealql/functions/database/meta). Their behaviour has not changed.

These functions can be used to retrieve specific metadata from a SurrealDB Record ID.

| Function | Description |
| --- | --- |
| record::exists() | Checks to see if a SurrealDB Record ID exists |
| record::id() | Extracts and returns the identifier from a SurrealDB Record ID |
| record::tb() | Extracts and returns the table name from a SurrealDB Record ID |
| record::refs() | Extracts and returns the record IDs of any records that have a record link along with a REFERENCES clause |
| record::is_edge() | Identifies whether the value passed in is a graph edge |


## record::exists


The `record::exists` function checks to see if a given record exists.

API DEFINITION

```
record::exists(record) -> bool

```

A simple example showing the output of this function when a record does not exist and when it does:

```
RETURN record::exists(r"person:tobie");
-- false

CREATE person:tobie;
RETURN record::exists(r"person:tobie");
-- true

```

A longer example of `record::exists` using method syntax:

```
FOR $person IN ["Haakon_VII", "Ferdinand_I", "Manuel_II", "Wilhelm_II", "George_I", "Albert_I", "Alfonso_XIII", "George_V", "Frederick_VIII"] {
    LET $record_name = type::record("person", $person.lowercase());
    IF !$record_name.exists() {
        CREATE $record_name;
    }
}

```

## record::id


The `record::id` function extracts and returns the identifier from a SurrealDB Record ID.

API DEFINITION

```
record::id(record) -> value

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN record::id(person:tobie);

'tobie'

```

## record::tb


The `record::tb` function extracts and returns the table name from a SurrealDB Record ID.

API DEFINITION

```
record::tb(record) -> string

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN record::tb(person:tobie);

-- 'person'

```


## record::is_edge


The `record::is_edge` function checks to see if the value passed in is a graph edge.

API DEFINITION

```
record::is_edge(record | string) -> bool

```

```
RELATE person:one->likes:first_like->person:two;

-- Both return true
record::is_edge(likes:first_like);
record::is_edge("likes:first_like");

```

## Method chaining


Method chaining allows functions to be called using the `.` dot operator on a value of a certain type instead of the full path of the function followed by the value.

```
-- Traditional syntax
record::id(r"person:aeon");

-- Method chaining syntax
r"person:aeon".id();

```

Response

```
'aeon'

```

This is particularly useful for readability when a function is called multiple times.

```
-- Traditional syntax
record::table(array::max([r"person:aeon", r"person:landevin"]));

-- Method chaining syntax
[r"person:aeon", r"person:landevin"].max().table();

```

Response

```
'person'

```
