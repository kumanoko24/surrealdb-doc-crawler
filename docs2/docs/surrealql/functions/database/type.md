---
title: Type Functions
url: https://surrealdb.com/docs/surrealql/functions/database/type
crawled_at: 2026-03-25 19:10:06
---

# Type Functions

###### Note

Since version 3.0.0-beta, the `::is::` functions (e.g. `type::is::record()`) now use underscores (e.g. `type::is_record()`) to better match the intent of the function and method syntax.

These functions can be used for generating and coercing data to specific data types. These functions are useful when accepting input values in client libraries, and ensuring that they are the desired type within SQL statements.


| Function |Description | |
| `type::array()` |Converts a value into an array | |
| `type::bool()` |Converts a value into a boolean | |
| `type::bytes()` |Converts a value into bytes | |
| `type::datetime()` |Converts a value into a datetime | |
| `type::decimal()` |Converts a value into a decimal | |
| `type::duration()` |Converts a value into a duration | |
| `type::field()` |Projects a single field within a SELECT statement | |
| `type::fields()` |Projects a multiple fields within a SELECT statement | |
| `type::file()` |Converts two strings into a file pointer | |
| `type::float()` |Converts a value into a floating point number | |
| `type::int()` |Converts a value into an integer | |
| `type::number()` |Converts a value into a number | |
| `type::of()` |Returns the type of a value | |
| `type::point()` |Converts a value into a geometry point | |
| `type::record()` |Converts a value into a record pointer | |
| `type::string()` |Converts a value into a string | |
| `type::table()` |Converts a value into a table | |
| `type::range()` |Converts a value into a range | |
| `type::uuid()` |Converts a value into a UUID | |
| `type::is_array()` |Checks if given value is of type array | |
| `type::is_bool()` |Checks if given value is of type bool | |
| `type::is_bytes()` |Checks if given value is of type bytes | |
| `type::is_collection()` |Checks if given value is of type collection | |
| `type::is_datetime()` |Checks if given value is of type datetime | |
| `type::is_decimal()` |Checks if given value is of type decimal | |
| `type::is_duration()` |Checks if given value is of type duration | |
| `type::is_float()` |Checks if given value is of type float | |
| `type::is_geometry()` |Checks if given value is of type geometry | |
| `type::is_int()` |Checks if given value is of type int | |
| `type::is_line()` |Checks if given value is of type line | |
| `type::is_none()` |Checks if given value is of type none | |
| `type::is_null()` |Checks if given value is of type null | |
| `type::is_multiline()` |Checks if given value is of type multiline | |
| `type::is_multipoint()` |Checks if given value is of type multipoint | |
| `type::is_multipolygon()` |Checks if given value is of type multipolygon | |
| `type::is_number()` |Checks if given value is of type number | |
| `type::is_object()` |Checks if given value is of type object | |
| `type::is_point()` |Checks if given value is of type point | |
| `type::is_polygon()` |Checks if given value is of type polygon | |
| `type::is_range()` |Checks if given value is of type range | |
| `type::is_record()` |Checks if given value is of type record | |
| `type::is_string()` |Checks if given value is of type string | |
| `type::is_uuid()` |Checks if given value is of type uuid | |
## `type::array`

The `type::array` function converts a value into an array.

API DEFINITION

```type::array(array|range) -> array

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::array(1..=3);

-- [1, 2, 3]

```

This is the equivalent of using [`<array>` to cast a value to an array.

## `type::bool`

The `type::bool` function converts a value into a boolean.

API DEFINITION

```type::bool(bool|string) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::bool("true");

-- true

```

This is the equivalent of using [`<bool>` to cast a value to a boolean.


## `type::bytes`

The `type::bytes` function converts a value into bytes.

API DEFINITION

```type::bytes(bytes|string) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::bytes("A few bytes");

-- b"4120666577206279746573"

```

This is the equivalent of using [`<bytes>` to cast a value to bytes.


## `type::datetime`

The `type::datetime` function converts a value into a datetime.

API DEFINITION

```type::datetime(datetime|string) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::datetime("2022-04-27T18:12:27+00:00");

-- d'2022-04-27T18:12:27Z'

```

This is the equivalent of using [`<datetime>` to cast a value to a datetime.


## `type::decimal`

The `type::decimal` function converts a value into a decimal.

API DEFINITION

```type::decimal(decimal|float|int|number|string) -> decimal

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::decimal("12345");

-- 12345dec

```

This is the equivalent of using [`<decimal>` to cast a value to a decimal.


## `type::duration`

The `type::duration` function converts a value into a duration.

API DEFINITION

```type::duration(duration|string) -> duration

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::duration("4h");

-- 4h

```

This is the equivalent of using [`<duration>` to cast a value to a duration.


## `type::field`

The `type::field` function projects a single field within a SELECT statement.

API DEFINITION

```type::field(string)

```

The following example shows this function, and its output:

```CREATE person:test SET title = 'Mr', name.first = 'Tobie', name.last = 'Morgan Hitchcock';

LET $param = 'name.first';

SELECT type::field($param), type::field('name.last') FROM person;

SELECT VALUE { 'firstname': type::field($param), lastname: type::field('name.last') } FROM person;

SELECT VALUE [type::field($param), type::field('name.last')] FROM person;

```

Output

```[
	{
		id: person:test,
		title: 'Mr',
		name: {
			first: 'Tobie',
			last: 'Morgan Hitchcock',
	    }
	}
]

```


This function can be used after the `OMIT` clause of a `SELECT` statement.

```LET $omit = "id";
CREATE person SET name = "Galen", surname = "Pathwarden", age = 19;
SELECT * OMIT type::field($omit) FROM person;

```

Output

```[
	{
		age: 19,
		name: 'Galen',
		surname: 'Pathwarden'
	}
]

```


## `type::fields`

The `type::fields` function projects one or more fields within a SELECT statement.

API DEFINITION

```type::fields(array<string>)

```

The following example shows this function, and its output:

```CREATE person:test SET title = 'Mr', name.first = 'Tobie', name.last = 'Morgan Hitchcock';

LET $param = ['name.first', 'name.last'];

SELECT type::fields($param), type::fields(['title']) FROM person;

SELECT VALUE { 'names': type::fields($param) } FROM person;

SELECT VALUE type::fields($param) FROM person;

```

Output

```[
	{
		id: person:test,
		title: 'Mr',
		name: {
			first: 'Tobie',
			last: 'Morgan Hitchcock',
		}
	}
]

```


This function can be used after the `OMIT` clause of a `SELECT` statement.

```LET $omit = ["id", "age"];
CREATE person SET name = "Galen", surname = "Pathwarden", age = 19;
SELECT * OMIT type::fields($omit) FROM person;

```

Output

```[
	{
		name: 'Galen',
		surname: 'Pathwarden'
	}
]

```


## `type::file`

The `type::file` function converts two strings representing a bucket name and a key into a [file pointer.

API DEFINITION

```type::file($bucket: string, $key: string) -> file

```

An example of a file pointer created using this function:

```type::file("my_bucket", "file_name")

```

Output

```f"my_bucket:/file_name"

```

The following query shows the equivalent file pointer when created using the `f` prefix:

```type::file("my_bucket", "file_name") == f"my_bucket:/file_name";

-- true

```

Once a [bucket has been defined, operations using one of the [file functions can be performed on the file pointer.

```DEFINE BUCKET my_bucket BACKEND "memory";

type::file("my_bucket", "file_name").put("Some data inside");
type::file("my_bucket", "file_name").get();

```

Output

```b"536F6D65206461746120696E73696465"

```


## `type::float`

The `type::float` function converts a value into a float.

API DEFINITION

```type::float(decimal|float|int|number|string) -> float

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::float("12345");

-- 12345f

```

This is the equivalent of using [`<float>` to cast a value to a float.


## `type::int`

The `type::int` function converts a value into an integer.

API DEFINITION

```type::int(decimal|float|int|number|string) -> int

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::int("12345");

-- 12345

```

This is the equivalent of using [`<int>` to cast a value to a int.


## `type::number`

The `type::number` function converts a value into a number.

API DEFINITION

```type::number(decimal|float|int|number|string) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::number("12345");

-- 12345

```

This is the equivalent of using [`<number>` to cast a value to a number.


## `type:of`

The `type::of` function returns a string denoting the type of a value.

API DEFINITION

```type::of(value) -> string

```

```type::of(2022dec);        -- 'decimal';
type::of(["some", 9]);    -- 'array';
type::of((50.0, 9.9));    -- 'geometry<point>'

```

## `type::point`

The `type::point` function converts a value into a geometry point.

API DEFINITION

```type::point(array|point) -> point

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::point([ 51.509865, -0.118092 ]);

-- (51.509865, -0.118092)

```


## `type::range`

The `type::range` function converts a value into a [range. It accepts a single argument, either a range or an array with two values. If the argument is an array, it will be converted into a range, similar to [casting.

API DEFINITION

```type::range(range|array) -> range<record>

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::range([1, 2]);
-- 1..2

RETURN type::range(1..10);
-- 1..10

RETURN type::range([1,9,4]);
-- 'Expected a range but cannot convert [1, 9, 4] into a range'

```


## `type::record`

###### Note

This function was known as `type::thing` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::record` function converts a value into a record pointer definition.

API DEFINITION

```type::record($table: any, $key: any) -> record

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```LET $tb = "person";
LET $id = "tobie";
RETURN type::record($tb, $id);

```

An example of this function being used to turn an array of objects into records to be created or upserted:

```FOR $data IN [
	{
		id: 9,
		name: 'Billy'
	},
	{
		id: 10,
		name: 'Bobby'
	}
] {
	UPSERT type::record('person', $data.id) CONTENT $data;
};

```

An example of the same except in which the `num` field is to be used as the record's ID. In this case, it can be mapped with the [`array::map()` function to rename `num` as `id` so that the following `CONTENT` clause does not create both a `num` and an `id` with the same value.

```FOR $data IN [
	{
		name: 'Billy',
		num: 9
	},
    {
		name: 'Bobby',
		num: 10
	},
].map(|$o| {
    id: $o.num,
    name: $o.name
}) {
    UPSERT type::record('person', $data.id) CONTENT $data;
};

```

If the second argument passed into `type::record` is a record ID, the latter part of the ID (the record identifier) will be extracted and used.

```type::record("person", person:mat);

-- person:mat

```

The output of the above function call will thus be `person:mat`, not `person:person:mat`.

The `type::record` function returns a record from a record or a string, with an optional argument to confirm the table name.

API DEFINITION

```type::record($record: record|string, $table_name: option<string>) -> record

```

The function will return a record as long as the argument passed in is already a record, or a string that can be parsed into one.

```-- Both return person:tobie
type::record(person:tobie);
type::record('person:tobie');

```

The optional second argument allows an assertation that the record passed in is of this table name.

```type::record('person:tobie', 'person'); -- person:tobie
type::record('person:tobie', 'cat'); -- "Expected a record<cat> but cannot convert 'person:tobie' into a record<cat>"

```

This second argument is mostly useful when involving a parameter that may or may not be a certain value. In the code below, the function may or may not err depending on whether the `$record` parameter is a `person` or a `cat` record.

```LET $record = rand::enum(person:tobie, cat:tobie);
type::record($record, 'person');

```


## `type::string`

The `type::string` function converts any value except `NONE`, `NULL`, and `bytes` into a string.

API DEFINITION

```type::string(any) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::string(12345);

-- '12345'

```

This is the equivalent of using [`<string>` to cast a value to a string.


## `type::string_lossy`

The `type::string_lossy` function converts any value except `NONE`, `NULL`, and `bytes` into a string. In the case of bytes, it will not return an error if the bytes are not valid UTF-8. Instead, invalid bytes will be replaced with the character `�` (`U+FFFD REPLACEMENT CHARACTER`, used in Unicode to represent a decoding error).

API DEFINITION

```type::string(any) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```-- Contains some invalid bytes
type::string_lossy(<bytes>[83, 117, 114, 255, 114, 101, 97, 254, 108, 68, 66]);
-- valid bytes
type::string_lossy(<bytes>[ 83, 117, 114, 114, 101, 97, 108, 68, 66 ]);

```

Output

```-------- Query --------

'Sur�rea�lDB'

-------- Query --------

'SurrealDB'

```

This is similar to using [`<string>` to cast a value to a string, except that an input of bytes will not fail.


## `type::table`

The `type::table` function converts a value into a table name.

API DEFINITION

```type::table(record|string) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN [
  type::table("person"),
  type::table(cat:one)
];

-- [person, cat]

```

As of version 2.0, SurrealDB no longer eagerly parses strings into record IDs. As such, the output of the last item ("dog:two") in the following example will differ. In version 1.x, it will be eagerly parsed into a record ID after which the `dog` table name will be returned, while in version 2.x it will be treated as a string and converted into the table name `dog:two`.

```RETURN [
  type::table(55),
  type::table(cat:one),
  type::table("dog"),
  type::table("dog:two"),
];

```

Output (V1.x)

```[
	`55`,
	cat,
	dog,
	dog
]

```

Output (V2.x)

```[
	`55`,
	cat,
	dog,
	`dog:two`
]

```


## `type::uuid`

The `type::uuid` function converts a value into a UUID.

API DEFINITION

```type::uuid(string|uuid) -> uuid

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::uuid("0191f946-936f-7223-bef5-aebbc527ad80");

-- u'0191f946-936f-7223-bef5-aebbc527ad80'

```


## `type::is_array`

###### Note

This function was known as `type::is::array` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_array` function checks if the passed value is of type `array`.

API DEFINITION

```type::is_array(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_array([ 'a', 'b', 'c' ]);

-- true

```


## `type::is_bool`

###### Note

This function was known as `type::is::bool` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_bool` function checks if the passed value is of type `bool`.

API DEFINITION

```type::is_bool(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_bool(true);

-- true

```


## `type::is_bytes`

###### Note

This function was known as `type::is::bytes` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_bytes` function checks if the passed value is of type `bytes`.

API DEFINITION

```type::is_bytes(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_bytes("I am not bytes");

-- false

```


## `type::is_collection`

###### Note

This function was known as `type::is::collection` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_collection` function checks if the passed value is of type `collection`.

API DEFINITION

```type::is_collection(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_collection("I am not a collection");

-- false

```


## `type::is_datetime`

###### Note

This function was known as `type::is::datetime` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_datetime` function checks if the passed value is of type `datetime`.

API DEFINITION

```type::is_datetime(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_datetime(time::now());

-- true

```


## `type::is_decimal`

###### Note

This function was known as `type::is::decimal` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_decimal` function checks if the passed value is of type `decimal`.

API DEFINITION

```type::is_decimal(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_decimal(<decimal> 13.5719384719384719385639856394139476937756394756);

-- true

```


## `type::is_duration`

###### Note

This function was known as `type::is::duration` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_duration` function checks if the passed value is of type `duration`.

API DEFINITION

```type::is_duration(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_duration('1970-01-01T00:00:00');

-- false

```


## `type::is_float`

###### Note

This function was known as `type::is::float` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_float` function checks if the passed value is of type ` float`.

API DEFINITION

```type::is_float(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_float(<float> 41.5);

-- true

```


## `type::is_geometry`

###### Note

This function was known as `type::is::geometry` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_geometry` function checks if the passed value is of type `geometry`.

API DEFINITION

```type::is_geometry(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_geometry((-0.118092, 51.509865));

-- true

```


## `type::is_int`

###### Note

This function was known as `type::is::int` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_int` function checks if the passed value is of type `int`.

API DEFINITION

```type::is_int(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_int(<int> 123);

-- true

```


## `type::is_line`

###### Note

This function was known as `type::is::line` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_line` function checks if the passed value is of type `line`.

API DEFINITION

```type::is_line(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_line("I am not a line");

-- false

```


## `type::is_none`

###### Note

This function was known as `type::is::none` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_none` function checks if the passed value is of type `none`.

API DEFINITION

```type::is_none(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_none(NONE);

-- true

```


## `type::is_null`

###### Note

This function was known as `type::is::null` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_null` function checks if the passed value is of type `null`.

API DEFINITION

```type::is_null(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_null(NULL);

-- true

```


## `type::is_multiline`

###### Note

This function was known as `type::is::multiline` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_multiline` function checks if the passed value is of type `multiline`.

API DEFINITION

```type::is_multiline(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_multiline("I am not a multiline");

-- false

```


## `type::is_multipoint`

###### Note

This function was known as `type::is::multipoint` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_multipoint` function checks if the passed value is of type `multipoint`.

API DEFINITION

```type::is_multipoint(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_multipoint("I am not a multipoint");

-- false

```


## `type::is_multipolygon`

###### Note

This function was known as `type::is::multipolygon` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_multipolygon` function checks if the passed value is of type `multipolygon`.

API DEFINITION

```type::is_multipolygon(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_multipolygon("I am not a multipolygon");

-- false

```


## `type::is_number`

###### Note

This function was known as `type::is::number` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_number` function checks if the passed value is of type `number`.

API DEFINITION

```type::is_number(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_number(123);

-- true

```


## `type::is_object`

###### Note

This function was known as `type::is::object` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_object` function checks if the passed value is of type `object`.

API DEFINITION

```type::is_object(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_object({ hello: 'world' });

-- true

```


## `type::is_point`

###### Note

This function was known as `type::is::point` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_point` function checks if the passed value is of type `point`.

API DEFINITION

```type::is_point(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_point((-0.118092, 51.509865));

-- true

```


## `type::is_polygon`

###### Note

This function was known as `type::is::polygon` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_polygon` function checks if the passed value is of type `polygon`.

API DEFINITION

```type::is_polygon(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_polygon("I am not a polygon");

-- false

```

## `type::is_range`

###### Note

This function was known as `type::is::range` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_range` function checks if the passed value is of type `range`.

API DEFINITION

```type::is_range(any) -> bool

```

```type::is_range(0..1);
-- true

// method syntax
(0..1).is_range();
-- true

```

## `type::is_record`

###### Note

This function was known as `type::is::record` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_record` function checks if the passed value is of type `record`.

API DEFINITION

```type::is_record(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_record(user:tobie);

-- true

```

### Validate a table

Check if user:tobie is a record on the test table

```RETURN type::is_record(user:tobie, 'test');

-- false

```


## `type::is_string`

###### Note

This function was known as `type::is::string` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_string` function checks if the passed value is of type `string`.

API DEFINITION

```type::is_string(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_string("abc");

-- true

```


## `type::is_uuid`

###### Note

This function was known as `type::is::uuid` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `type::is_uuid` function checks if the passed value is of type `uuid`.

API DEFINITION

```type::is_uuid(any) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN type::is_uuid(u"018a6680-bef9-701b-9025-e1754f296a0f");

-- true

```


## Method chaining

Method chaining allows functions to be called using the `.` dot operator on a value of a certain type instead of the full path of the function followed by the value.

```-- Traditional syntax
type::is_record(r"person:aeon", "cat");

-- Method chaining syntax
r"person:aeon".is_record("cat");

```

Response

```false

```
