---
title: Rand functions
url: https://surrealdb.com/docs/surrealql/functions/database/rand
crawled_at: 2026-03-25 19:09:49
---

# Rand functions

These functions can be used when generating random data values.


| Function |Description | |
| `rand()` |Generates and returns a random floating point number | |
| `rand::bool()` |Generates and returns a random boolean | |
| `rand::duration()` |Generates and returns a random duration | |
| `rand::enum()` |Randomly picks a value from the specified values | |
| `rand::float()` |Generates and returns a random floating point number | |
| `rand::id()` |Generates and returns a random id | |
| `rand::int()` |Generates and returns a random integer | |
| `rand::string()` |Generates and returns a random string | |
| `rand::time()` |Generates and returns a random datetime | |
| `rand::uuid()` |Generates and returns a random UUID | |
| `rand::uuid::v4()` |Generates and returns a random Version 4 UUID | |
| `rand::ulid()` |Generates and returns a random ULID | |
## `rand`

The rand function generates a random [`float`, between 0 and 1.

API DEFINITION

```rand() -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN rand();

0.7062321084863658

```

The following example shows this function being used in a [`SELECT` statement with an `ORDER BY` clause:

```SELECT * FROM [{ age: 33 }, { age: 45 }, { age: 39 }] ORDER BY rand();


[
	{
		age: 45
	},
	{
		age: 39
	},
	{
		age: 33
	}
]

```


## `rand::bool`

The rand::bool function generates a random [`boolean` value.

API DEFINITION

```rand::bool() -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN rand::bool();

true

```


## `rand::duration`

The rand::duration function generates a random [`duration` value between two `duration` arguments.

API DEFINITION

```rand::bool($from: duration, $to: duration) -> duration

```

Some examples of the function in use:

```rand::duration(1ns, 1ms);

rand::duration(0ns, duration::max);

```

Output

```-------- Query 1 --------
435µs884ns

-------- Query 2 --------
405337457164y36w2d5h54m8s16ms76µs191ns

```


## `rand::enum`

The `rand::enum` function generates a random value, from a multitude of values.

API DEFINITION

```rand::enum(value...) -> any
rand::enum(array<value>) -> any

```

The argument to this function can take either comma-separated values or an array of values.

```rand::enum('one', 'two', 3, 4.15385, 'five', true);
rand::enum(['one', 'two', 3, 4.15385, 'five', true]);

"five"

```

As nested values are not combined at greater levels of depth, the following example will return either `[8, 9]` or `[10, 11]`, but never an individual number.

```RETURN rand::enum([
    [8,9],
    [10,11]
]);

```


## `rand::float`

The `rand::float` function generates a random [`float`, between `0` and `1`.

API DEFINITION

```rand::float() -> float

```

If two numbers are provided, then the function generates a random [`float`, between two numbers.

API DEFINITION

```rand::float($from: number, $to: number) -> float

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN rand::float();

0.7812733136200293

```

```RETURN rand::float(10, 15);

11.305355983514927

```


## `rand::id`

###### Note

This function was known as `rand::guid` in versions of SurrrealDB before 3.0.0-beta. The behaviour has not changed.

The `rand::id` function generates a random alphanumeric ID, defaulting to a length of 20 characters.

API DEFINITION

```rand::id() -> string

```

If a number is provided, then the function generates a random ID with a specific length.

API DEFINITION

```rand::id(number) -> string

```

If a second number is provided, then the function will generate a random id, with a length between the two numbers.

API DEFINITION

```rand::id($min_len: int, $max_len: int) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

Default 20-char random id

```RETURN rand::id();

'4uqmrmtjhtjeg77et0dl'

```

A 10-char random id

```RETURN rand::id(10);

'f3b6cjh0nt'

```

A random id with a length between 1 and 9 chars

```RETURN rand::id(1, 9);

'894bqt4lp'

```

This function is used for default record ID keys in SurrealDB, and can be overridden to use a ULID or UUID instead by affixing `:ulid()` and `:uuid()` after the table name, respectively.

```CREATE 
  person,
  person:ulid(),
  person:uuid()
-- Return only id values for nicer output
RETURN VALUE id;

```

Output:

```[
	person:o9s1sl3ivckuxo0kglix,
	person:01K7JRP6KVAQGN2THR2T13X9WP,
	person:u'0199e58b-1a7b-7880-ad5b-01671678c11f'
]

```


## `rand::int`

The `rand::int` function generates a random int.

API DEFINITION

```rand::int() -> int

```

If two numbers are provided, then the function generates a random int between two numbers.

API DEFINITION

```rand::int($from: int, $to: int) -> int

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN rand::int();

6841551695902514727

```

```RETURN rand::int(10, 15);

13

```


## `rand::string`

The `rand::string` function generates a random string, with 32 characters.

API DEFINITION

```rand::string() -> string

```

The `rand::string` function generates a random string, with a specific length.

API DEFINITION

```rand::string(number) -> string

```

If two numbers are provided, then the function generates a random string, with a length between two numbers.

API DEFINITION

```rand::string($from: int, $to: int) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN rand::string();

"N8Q86mklN6U7kv0A2XCRh5UlpQMSvdoT"

```

```RETURN rand::string(15);

"aSCtrfJj4pSJ7Xq"

```

```RETURN rand::string(10, 15);

"rEUWFUMcx0YH"

```


## `rand::time`

The `rand::time` function generates a random [`datetime`.

API DEFINITION

```rand::time() -> datetime
rand::time($from: datetime|number, $to: datetime|number) -> datetime

```

The rand::time function generates a random [`datetime`, either a completely random datetime when no arguments are passed in, or between two unix timestamps.

```RETURN rand::time();

-- d'1327-07-12T01:00:32Z'

RETURN rand::time(198371, 1223138713);

-- d'1991-01-13T23:27:17Z'

```

This function can take two datetimes, returning a random datetime in between the least and greatest of the two.

```RETURN rand::time(d'1970-01-01', d'2000-01-01');

-- d'1999-05-29T17:02:16Z"

```

Either of the arguments of this function can now be either a number or a datetime.

```RETURN rand::time(0, d'1990-01-01');

-- d'1986-11-17T15:06:01Z'

```

As of this version, this function returns a datetime between 0000-01-01T00:00:00Z and 9999-12-31T23:59:59Z. Before this, the function returned a random datetime between 1970-01-01T00:00:00Z (0 seconds after the UNIX epoch) and +262142-12-31T23:59:59Z (the maximum possible value for a `datetime`).

## `rand::uuid`

The `rand::uuid` function generates a random Version 7 UUID.

API DEFINITION

```rand::uuid() -> uuid
rand::uuid(datetime) -> uuid

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN rand::uuid();

[u"e20b2836-e689-4643-998d-b17a16800323"]

```

The `rand::uuid` function can also generate a random UUID from a datetime.

```RETURN rand::uuid(d"2021-09-07T04:27:53Z");

```

Note that a UUID has a precision of one millisecond, and thus one converted back to a datetime will truncate nanosecond precision.

```LET $now = time::now();
[$now, time::from_uuid(rand::uuid($now))];

-- Output:
[
	d'2026-01-29T02:14:10.057075Z',
	d'2026-01-29T02:14:10.057Z'
]

```

The `rand::uuid` function can also be called using its alias `rand::uuid::v7`.


## `rand::uuid::v4`

The `rand::uuid::v4` function generates a random version 4 UUID.

API DEFINITION

```rand::uuid::v4() -> uuid

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN rand::uuid::v4();

[u"4def23a5-a847-4934-8dad-c64ccc48921b"]

```


## `rand::ulid`

The `rand::ulid` function generates a random ULID.

API DEFINITION

```rand::ulid() -> uuid
rand::ulid(datetime) -> uuid

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN rand::ulid();

[u"01H9QDG81Q7SB33RXB7BEZBK7G"]

```

The `rand::ulid` function can also generate a random ULID from a datetime type.

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN rand::ulid(d"2021-09-07T04:27:53Z");

```

Note that a ULID has a precision of one millisecond, and thus one converted back to a datetime will truncate nanosecond precision.

```LET $now = time::now();
[$now, time::from_ulid(rand::ulid($now))];

-- Output:
[
	d'2026-01-29T02:14:10.057075Z',
	d'2026-01-29T02:14:10.057Z'
]

```
