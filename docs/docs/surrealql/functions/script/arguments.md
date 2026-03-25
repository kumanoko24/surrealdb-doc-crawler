---
title: Arguments
url: https://surrealdb.com/docs/surrealql/functions/script/arguments
crawled_at: 2026-03-25 18:43:38
---

# Arguments


Additional arguments can be passed in to the function from SurrealDB, and these are accessible as an array using the `arguments` object within the JavaScript function.

```
-- Create a new parameterLET $val = "SurrealDB";-- Create a new parameterLET $words = ["awesome", "advanced", "cool"];-- Pass the parameter values into the functionCREATE article SET summary = function($val, $words) {	const [val, words] = arguments;	return `${val} is ${words.join(', ')}`;};
```
