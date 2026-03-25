---
title: LIMIT clause
url: https://surrealdb.com/docs/surrealql/clauses/limit
crawled_at: 2026-03-25 18:41:51
---

# LIMIT clause


The `LIMIT` clause is used to limit the number of records returned by a query. It is particularly useful when you want to retrieve a specific number of records from a table.

When using the `LIMIT` clause, it is possible to paginate results by using the `START` clause to start from a specific record from the result set. It is important to note that the `START` count starts from 0.

## Syntax


Clause Syntax

```
LIMIT @number [START @start 0]
```

## Examples


```
-- Select the first 10 recordsSELECT * FROM person LIMIT 10;-- Start at record 50 and select the following 10 recordsSELECT * FROM person LIMIT 10 START 50;
```

```
-- Select the first 5 records from the arraySELECT * FROM [1,2,3,4,5,6,7,8,9,10] LIMIT 5 START 4;
```

Result

```
[	5,	6,	7,	8,	9]
```

The `LIMIT` clause followed by `1` is often used along with the `ONLY` clause to satisfy the requirement that only up to a single record can be returned.

```
-- Record IDs are unique so guaranteed to be no more than 1SELECT * FROM ONLY person:jamie;-- Error because no guarantee that this will return a single recordSELECT * FROM ONLY person WHERE name = "Jaime";-- Add `LIMIT 1` to ensure that only up to one record will be returnedSELECT * FROM ONLY person WHERE name = "Jaime" LIMIT 1;
```
