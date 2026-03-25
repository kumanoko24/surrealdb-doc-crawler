---
title: Bytes
url: https://surrealdb.com/docs/surrealql/datamodel/bytes
crawled_at: 2026-03-25 19:08:50
---

# Bytes

Bytes can be created by casting from a string, and are displayed using hexidecimal encoding.

```<bytes>"I am some bytes";

```

Output

```b"4920616D20736F6D65206279746573"

```

## Conversion from other types

Since SurrealDB 2.3.0, conversions can be performed between bytes, strings, and arrays.

```-- array<int> to bytes to string
<string><bytes>[ 99, 101, 108, 108, 97, 114, 32, 100, 111, 111, 114 ];
-- string to bytes to array<int>
<array><bytes>"Hobbits";

```

Output

```-------- Query --------

'cellar door'

-------- Query --------

[ 72, 111, 98, 98, 105, 116, 115 ]

```

## Byte strings

A string preceded by a `b` prefix can be turned into bytes as long as the string represents a hexidecimal value.

```b"486F6262697473";

<string>b"486F6262697473";

<string>b"This won't work though";

```

Output

```-------- Query --------

b"486F6262697473";

-------- Query --------

'Hobbits'

-------- Query --------

"There was a problem with the database: Parse error: Unexpected character `T` expected hexidecimal digit
 --> [1:11]
  |
1 | <string>b\"This won't work though\";
  |           ^ 
"

```
