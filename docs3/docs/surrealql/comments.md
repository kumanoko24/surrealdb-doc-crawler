---
title: Comments
url: https://surrealdb.com/docs/surrealql/comments
crawled_at: 2026-03-25 21:43:03
---

# Comments


In SurrealQL, comments can be written in a number of different ways.

```
/*
In SurrealQL, comments can be written as single-line
or multi-line comments, and comments can be used and
interspersed within statements.
*/

SELECT * FROM /* get all users */ user;

# There are a number of ways to use single-line comments
SELECT * FROM user;

// Alternatively using two forward-slash characters
SELECT * FROM user;

-- Another way is to use two dash characters
SELECT * FROM user;

```
