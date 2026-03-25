---
title: Sequence functions
url: https://surrealdb.com/docs/surrealql/functions/database/sequence
crawled_at: 2026-03-25 19:08:57
---

# Sequence functions

These functions can be used to work with [sequences.


| Function |Description | |
| `sequence::next()` |Returns the next value in a sequence. | |
## `sequence::next`

The `sequence::next` function returns the next value in a sequence.

API DEFINITION

```sequence::next($seq_name: string) -> int

```

```DEFINE SEQUENCE mySeq2 BATCH 1000 START 100 TIMEOUT 5s;
sequence::nextval('mySeq2');

-- 100

```
