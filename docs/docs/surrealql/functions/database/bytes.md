---
title: Bytes functions
url: https://surrealdb.com/docs/surrealql/functions/database/bytes
crawled_at: 2026-03-25 18:42:58
---

# Bytes functions


These functions can be used when working with bytes in SurrealQL.

| Function | Description |
| --- | --- |
| bytes::len() | Gives the length in bytes |


## bytes::len


The `bytes::len` function returns the length in bytes of a `bytes` value.

API DEFINITION

```
bytes::len(bytes) -> int
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN [    bytes::len(<bytes>"Simple ASCII string"),    bytes::len(<bytes>"οὐ γὰρ δυνατόν ἐστιν ἔτι καθεύδειν"),    bytes::len(<bytes>"청춘예찬 靑春禮讚")];
```

Output

```
[ 19, 67, 25 ]
```
