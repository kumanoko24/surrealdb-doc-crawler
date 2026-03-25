---
title: Arguments
url: https://surrealdb.com/docs/surrealql/functions/script/arguments
crawled_at: 2026-03-25 21:42:54
---

# Arguments


Additional arguments can be passed in to the function from SurrealDB, and these are accessible as an array using the `arguments` object within the JavaScript function.

```
-- Create a new parameter
LET $val = "SurrealDB";
-- Create a new parameter
LET $words = ["awesome", "advanced", "cool"];
-- Pass the parameter values into the function
CREATE article SET summary = function($val, $words) {
	const [val, words] = arguments;
	return `${val} is ${words.join(', ')}`;
};

```
