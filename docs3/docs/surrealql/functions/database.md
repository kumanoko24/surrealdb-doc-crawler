---
title: Database Functions
url: https://surrealdb.com/docs/surrealql/functions/database
crawled_at: 2026-03-25 21:42:14
---

# Database Functions


SurrealDB has many built-in functions designed to handle many common database tasks and work with SurrealDB's various data types, grouped into modules based on their purpose and the data types they are designed to work with. The table below lists all of SurrealDB's function modules, with descriptions and links to their own detailed documentation.

| Function | Description and Example |
| --- | --- |
| API | These functions can be used to add middleware to a defined API endpoint. Example: api::timeout(1s) |
| Array | These functions can be used when working with, and manipulating arrays of data. Example: array::len([1,2,3]) |
| Bytes | These functions can be used when working with bytes in SurrealQL. Example: bytes::len("SurrealDB".to_bytes()); |
| Count | This function can be used when counting field values and expressions. Example: count([1,2,3]) |
| Crypto | These functions can be used when hashing data, encrypting data, and for securely authenticating users into the database. Example: crypto::argon2::generate("MyPaSSw0RD") |
| Duration | These functions can be used when converting between numeric and duration data. Example: duration::days(90h30m) |
| Encoding | These functions can be used to encode and decode data in base64. Example: encoding::base64::decode("aGVsbG8") |
| Files | These functions can be used to work with files. Example: f"my_bucket:/my_book.txt".get() |
| Geo | These functions can be used when working with and analysing geospatial data. Example: geo::distance((-0.04, 51.55), (30.46, -17.86)) |
| HTTP | These functions can be used when opening and submitting remote web requests, and webhooks. Example: http::get('https://surrealdb.com') |
| Math | These functions can be used when analysing numeric data and numeric collections. Example: math::max([ 26.164, 13.746189, 23, 16.4, 41.42 ]) |
| Meta | These functions can be used to retrieve specific metadata from a SurrealDB Record ID. As of version 2.0, these functions are deprecated and replaced with SurrealDB's record functions. |
| Not | This function reverses the truthiness of a value. Example: not(true) |
| Object | These functions can be used when working with, and manipulating data objects. Example: object::from_entries([[ "a", 1 ],[ "b", true ]]) |
| Parse | These functions can be used when parsing email addresses and URL web addresses. Example: parse::url::domain("http://127.0.0.1/index.html") |
| Rand | These functions can be used when generating random data values. Example: rand::enum('one', 'two', 3, 4.15385, 'five', true) |
| Record | These functions can be used to retrieve specific metadata from a SurrealDB Record ID. Example: record::id(person:tobie) |
| Search | These functions are used in conjunction with the @@ operator (the 'matches' operator) to either collect the relevance score or highlight the searched keywords within the content. Example: SELECT search::score(1) AS score FROM book WHERE title @1@ 'rust web' |
| Sequence | These functions can be used to work with a defined sequence. Example: sequence::nextval('mySeq2') |
| Session | These functions return information about the current SurrealDB session. Example: session::db() |
| Set | These functions can be used when working with, and manipulating sets of data. Example: `set::len({1,2,3})` |
| Sleep | This function can be used to introduce a delay or pause in the execution of a query or a batch of queries for a specific amount of time. Example: sleep(900ms) |
| String | These functions can be used when working with and manipulating text and string values. Example: string::reverse('emosewa si 0.2 BDlaerruS') |
| Time | These functions can be used when working with and manipulating datetime values. Example: time::timezone() |
| Type | These functions can be used for generating and coercing data to specific data types. Example: type::is_number(500) |
| Value | This module contains several miscellaneous functions that can be used with values of any type. Example: value::diff([true, false], [true, true]) |
| Vector | A collection of essential vector operations that provide foundational functionality for numerical computation, machine learning, and data analysis. Example: vector::add([1, 2, 3], [1, 2, 3]) |


## How to use database functions


### Classic syntax


Functions in SurrealDB can always be called using their full path names beginning with the package names indicated above, followed by the function arguments.

```
string::split("SurrealDB 2.0 is on its way!", " ");
array::len([1,2,3]);
type::is_number(10);
type::record("cat", "mr_meow");

```

Response

```
-------- Query --------

[
	'SurrealDB',
	'2.0',
	'is',
	'on',
	'its',
	'way!'
]

-------- Query --------

3

-------- Query --------

true

-------- Query --------

cat:mr_meow

```

### Method syntax


Functions that are called on an existing value can be called using method syntax, using the `.` (dot) operator.

The following functions will produce the same output as the classic syntax above. `type::record()` cannot be called with method syntax because it is used to outright create a record ID from nothing, rather than being called on an existing value.

```
"SurrealDB 2.0 is on its way!".split(" ");
[1,2,3].len();
10.is_number();

```

The method syntax is particular useful when calling a number of functions inside a single query.

```
array::len(array::windows(array::distinct(array::flatten([[1,2,3],[1,4,6],[4,2,4]])), 2));

```

Readability before `2.0` could be improved to a certain extent by moving a query of this type over multiple lines.

```
array::len(
    array::clump(
        array::distinct(
            array::flatten([[1,2,3],[1,4,6],[4,2,4]])
        )
    , 2)
);

```

However, method chaining syntax allows queries of this type to be read from left to right in a functional manner. This is known as method chaining. As each of the methods below except the last return an array, further array methods can thus be called by using the `.` operator. The final method then returns an integer.

```
[[1,2,3],[1,4,6],[4,2,4],2].flatten().distinct().windows(2).len();

```

This can be made even more readable by splitting over multiple lines.

```
[[1,2,3],[1,4,6],[4,2,4]]
    .flatten()
    .distinct()
    .windows(2)
    .len();

```

### Conversion from :: (double colon) to _ (underscore) syntax


Full function paths in SurrealDB were converted to match the method syntax detailed above.

```
-- Old syntax
type::is::record(person:one);
-- Method syntax
person:one.is_record();
-- New syntax now matches method syntax
type::is_record(person:one);

```

### Mathematical constants


The page on mathematical functions also contains a number of mathematical constants. They are used in a similar way to functions except that their paths point to hard-coded values instead of a function pointer and thus do not need parentheses.

```
RETURN [math::pi, math::tau, math::e];

```

Response

```
[
	3.141592653589793f,
	6.283185307179586f,
	2.718281828459045f
]

```

## Aggregate functions


A few functions can be used not just on their own but as part of a [pre-computed table view](/docs/surrealql/statements/define/table#pre-computed-table-views).

These functions are:

- count()
- math::max()
- math::min()
- math::sum()
- math::mean()
- math::stddev()
- math::variance()
- time::max()
- time::min()

## Anonymous functions


SurrealDB also allows for the creation of anonymous functions (also known as closures) that do not need to be defined on the database. See [the page on closures](/docs/surrealql/datamodel/closures) for more details.
