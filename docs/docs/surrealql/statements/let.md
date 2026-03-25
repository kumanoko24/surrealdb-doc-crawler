---
title: LET Statement
url: https://surrealdb.com/docs/surrealql/statements/let
crawled_at: 2026-03-25 18:41:20
---

# LET Statement


The `LET` statement allows you to create parameters to store any value, including the results of queries or the outputs of expressions. These parameters can then be referenced throughout your SurrealQL code, making your queries more dynamic and reusable.

## Syntax


The syntax for the `LET` statement is straightforward. The parameter name is prefixed with a `$` symbol.
SurrealQL SyntaxRailroad Diagram
SurrealQL Syntax

```
LET $@parameter [: @type_name] = @value;
```
LET$@parameter:@type_name=@value;
## Example Usage


### Basic Parameter Assignment


You can use the `LET` statement to store simple values or query results. For example, storing a string value and then using it in a `CREATE` statement:

```
-- Define the parameterLET $name = "tobie";-- Use the parameterCREATE person SET name = $name;
```

### Storing Query Results


The `LET` statement is also useful for storing the results of a query, which can then be used in subsequent operations:

```
-- Define the parameterLET $adults = SELECT * FROM person WHERE age > 18;-- Use the parameterUPDATE $adults SET adult = true;
```

### Conditional Logic with IF ELSE


SurrealQL allows you to define parameters based on conditional logic using `IF ELSE` statements:

```
LET $num = 10;LET $num_type =         IF type::is_int($num)     { "integer" }    ELSE IF type::is_decimal($num) { "decimal" }    ELSE IF type::is_float($num)   { "float"   };RETURN $num_type;-- 'integer'
```

## Anonymous Functions


You can define anonymous functions also known as closures using the `LET` statement. These functions can be used to encapsulate reusable logic and can be called from within your queries. Learn more about anonymous functions in the Data model section.

## Pre-Defined and Protected Parameters


SurrealDB comes with pre-defined parameters that are accessible in any context. However, parameters created using `LET` are not accessible within the scope of these pre-defined parameters.

Furthermore, some pre-defined parameters are protected and cannot be overwritten using `LET`:

```
LET $before = "Before!";-- Returns ["Before!"];RETURN $before;-- Returns the `person` records before deletionDELETE person RETURN $before;-- Returns "Before!" againRETURN $before;
```

Attempting to redefine protected parameters will result in an error:

```
LET $auth = 1;LET $session = 10;
```

Output

```
-------- Query 1 (0ns) --------"'auth' is a protected variable and cannot be set"-------- Query 2 (0ns) --------"'session' is a protected variable and cannot be set"
```

## Typed LET statements


Type safety in a `LET` statement can be ensured by adding a `:` (a colon) and the type name after the `LET` keyword.

```
LET $number: int = "9";
```

Output

```
"Tried to set `$number`, but couldn't coerce value: Expected `int` but found `'9'`"
```

### Taking advantage of type safety


Using typed `LET` statements is a good practice when prototyping code or when getting used to SurrealQL for the first time. Take the following example that attempts to count the number of `true` values in a field by filtering out values that are not `true`, without noticing that the field actually contains strings instead of booleans. The query output ends up being 0, rather than the expected 2.

```
CREATE some:record SET vals = ["true", "false", "true"];some:record.vals.filter(|$val| $val = true).len();
```

Output

```
0
```

Breaking this into multiple typed `LET` statements shows the error right away.

```
LET $vals: array<bool> = some:record.vals;LET $len: number = $vals.filter(|$val| $val = true).len();$len;
```

Output

```
-------- Query 1 --------"Tried to set `$vals`, but couldn't coerce value: Expected `bool` but found `'true'` when coercing an element of `array<bool>`"-------- Query 2 --------'There was a problem running the filter() function. no such method found for the none type'-------- Query 3 --------NONE
```

With the location of the error in clear sight, a fix is that much easier to implement.

```
-- Use .map() to turn each string into a boolLET $vals: array<bool> = some:record.vals.map(|$val| <bool>$val);LET $len: number = $vals.filter(|$val| $val = true).len();$len;
```

Output

```
2
```

### Typed literal statements


Multiple possible types can be specified in a `LET` statement by adding a `|` (vertical bar) in between each possible type.

```
LET $number: int | string = "9";
```

Even complex types such as objects can be included in a typed `LET` statement.

```
LET $error_info: string | { error: string } = { error: "Something went wrong plz help" };
```

For more information on this pattern, see the page on literals.

## Conclusion


The `LET` statement in SurrealDB is versatile, allowing you to store values, results from subqueries, and even define anonymous functions. Understanding how to use `LET` effectively can help you write more concise, readable, and maintainable queries.
