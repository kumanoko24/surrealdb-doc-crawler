---
title: SurrealQL functions
url: https://surrealdb.com/docs/surrealql/functions/script/surrealql-functions
crawled_at: 2026-03-25 18:43:44
---

# SurrealQL functions


Embedded scripting functions have access to native SurrealQL functions, allowing for complex and performant operations otherwise not possible. SurrealQL functions are published under the `surrealdb.functions` variable. Custom functions are not available within the embedded JavaScript function at the moment.

```
RETURN function() {	// Using the rand::uuid::v4() function	const uuid = surrealdb.functions.rand.uuid.v4();};
```
