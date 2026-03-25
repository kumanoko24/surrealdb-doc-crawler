---
title: Value functions
url: https://surrealdb.com/docs/surrealql/functions/database/value
crawled_at: 2026-03-25 19:09:32
---

# Value functions

This module contains several miscellaneous functions that can be used with values of any type.


| Function |Description | |
| `.chain()` |Allows an anonymous function to be called on a value | |
| `value::diff()` |Returns the operation required for one value to equal another | |
| `value::patch()` |Applies JSON Patch operations to a value | |
## `.chain()`

The `.chain()` method passes a value into a [closure through which an operation can be performed to return any value.

API DEFINITION

```value.chain(closure) -> value;

```

The output of this function is usually based on the value passed into the closure, but can be something else entirely.

```'SurrealDB'.chain(|$n| $n + ' 3.0');
-- 'SurrealDB 3.0'

'SurrealDB'.chain(|$n| "Something else");

```

The function is only called using the `.` operator (method syntax) and, as the name implies, works well within a chain of methods.

```{ company: 'SurrealDB', latest_version: '2.0' }
    .chain(|$name| <string>$name)
    .replace('SurrealDB', 'SURREALDB!!!!!');

```

Response

```"{ company: 'SURREALDB!!!!!', latest_version: '2.0' }"

```

For a similar function that allows using a closure on each item in an array instead of a value as a whole, see [array::map.

## `value::diff`

The `value::diff` function returns an object that shows the [JSON Patch operation(s) required for the first value to equal the second one.

API DEFINITION

```value::diff(value, $other: value) -> array<object>

```

The following is an example of the `value::diff` function used to display the changes required to change one string into another. Note that the JSON Patch spec requires an array of objects, and thus an array will be returned even if only one patch is needed between two values.

```RETURN 'tobie'.diff('tobias');

```

Output

```[
	{
		op: 'change',
		path: '/',
		value: '@@ -1,5 +1,6 @@
 tobi
-e
+as
'
	}
]

```

An example of the output when the diff output includes more than one operation:

```{ company: 'SurrealDB' }.diff({ company: 'SurrealDB!!', latest_version: '2.0', location: city:london });

```

Response

```[
	{
		op: 'change',
		path: '/company',
		value: '@@ -2,8 +2,10 @@
 urrealDB
+!!
'
	},
	{
		op: 'add',
		path: '/latest_version',
		value: '2.0'
	},
	{
		op: 'add',
		path: '/location',
		value: city:london
	}
]

```

## `value::patch`

The `value::patch` function applies an array of JSON Patch operations to a value.

API DEFINITION

```value::patch(value, $patch: array<object>) -> value

```

```LET $company = {
    company: 'SurrealDB',
    latest_version: '1.5.4'
};

$company.patch([{
		'op': 'replace',
		'path': 'latest_version',
		'value': '3.0'
}]);

```

Response

```{
	company: 'SurrealDB',
	version: '3.0'
}

```
