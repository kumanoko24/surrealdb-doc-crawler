---
title: Object functions
url: https://surrealdb.com/docs/surrealql/functions/database/object
crawled_at: 2026-03-25 19:08:34
---

# Object functions

These functions can be used when working with, and manipulating data objects.


| Function |Description | |
| `object::entries()` |Transforms an object into an array with arrays of key-value combinations. | |
| `object::extend()` |Extends an object with the content of another one. | |
| `object::from_entries()` |Transforms an array with arrays of key-value combinations into an object. | |
| `object::is_empty()` |Checks if an object is empty | |
| `object::keys()` |Returns an array with all the keys of an object. | |
| `object::len()` |Returns the amount of key-value pairs an object holds. | |
| `object::remove()` |Removes one or more fields from an object. | |
| `object::values()` |Returns an array with all the values of an object. | |
## `object::entries`

The `object::entries` function transforms an object into an array with arrays of key-value combinations.

API DEFINITION

```object::entries(object) -> array

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN object::entries({
  a: 1,
  b: true
});

```

Response

```[
  [ 'a', 1 ],
  [ 'b', true ],
]

```


## `object::extend`

The `object::extend` function extends an object with the fields and values of another one, essentially adding the two together.

API DEFINITION

```object::extend(object, $other: object) -> object

```

An example of the function, resulting in one new field (`gold`) and one updated field (`last_updated`) in the final output.

```{ name: "Mat Cauthon", last_updated: d'2013-01-08'}.extend( 
{ gold: 100, last_updated: time::now() });

```

Output

```{
	gold: 100,
	last_updated: d'2025-05-07T06:15:00.768Z',
	name: 'Mat Cauthon'
}

```

Note: the same behaviour can also be achieved using the `+` operator.

```{ name: "Mat Cauthon", last_updated: d'2013-01-08'} + 
{ gold: 100, last_updated: time::now() };

```


## `object::from_entries`

The `object::from_entries` function transforms an array with arrays of key-value combinations into an object.

API DEFINITION

```object::from_entries(array) -> object

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN object::from_entries([
  [ "a", 1 ],
  [ "b", true ],
]);

```

Response

```{
  a: 1,
  b: true
}

```

## `object::is_empty`

The `object::is_empty` function checks whether the object contains values.

API DEFINITION

```object::is_empty(object) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

An object that contain values

```RETURN {
  name: "Aeon",
  age: 20
}.is_empty();

-- false

```

An empty object

```RETURN object::is_empty({});

-- true

```

Example of `.is_empty()` being used in a [`DEFINE FIELD` statement to disallow empty objects:

```DEFINE FIELD metadata
  ON house
  TYPE object
  ASSERT !$value.is_empty();
CREATE house SET metadata = {};
CREATE house SET metadata = { floors: 5 };

```

Output

```-------- Query --------

'Found {  } for field `metadata`, with record `house:aei2fms2jccm46ceib8l`, but field must conform to: !$value.is_empty()'

-------- Query --------

[
	{
		id: house:g126ct3m0scbkockq32u,
		metadata: {
			floors: 5
		}
	}
]

```

## `object::keys`

The `object::keys` function returns an array with all the keys of an object.

API DEFINITION

```object::keys(object) -> array

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN object::keys({
  a: 1,
  b: true
});

-- [ 'a', 'b' ]

```


## `object::len`

The `object::len` function returns the amount of key-value pairs an object holds.

API DEFINITION

```object::len(object) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN object::len({
  a: 1,
  b: true
});

-- 2

```

## `object::remove`

The `object::remove` function removes one or more fields from an object.

API DEFINITION

```object::remove(object, $to_remove: string|array<string>) -> object

```

A single string can be used to remove a single field from an object, while an array of strings can be used to remove one or more fields at a time.

```{ name: "Mat Cauthon", last_updated: d'2013-01-08', gold: 100 }.remove("gold");
{ name: "Mat Cauthon", last_updated: d'2013-01-08', gold: 100 }.remove(["gold", "last_updated"]);

```

Output

```-------- Query 1 --------

{
	last_updated: d'2013-01-08T00:00:00Z',
	name: 'Mat Cauthon'
}

-------- Query 2 --------

{
	name: 'Mat Cauthon'
}

```

## `object::values`

The `object::values` function returns an array with all the values of an object.

API DEFINITION

```object::values(object) -> array

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN object::values({
  a: 1,
  b: true
});

-- [1, true]

```


## Method chaining

Method chaining allows functions to be called using the `.` dot operator on a value of a certain type instead of the full path of the function followed by the value.

```-- Traditional syntax
object::values({
  a: 1,
  b: true
});

-- Method chaining syntax
{
  a: 1,
  b: true
}.values();

```

Response

```[
  1,
  true
]

```

This is particularly useful for readability when a function is called multiple times.

```-- Traditional syntax
array::max(object::values(object::from_entries([["a", 1], ["b", 2]])));

-- Method chaining syntax
object::from_entries([["a", 1], ["b", 2]]).values().max();

```

Response

```2

```
