---
title: Anonymous functions (closures)
url: https://surrealdb.com/docs/surrealql/datamodel/closures
crawled_at: 2026-03-25 18:40:23
---

# Anonymous functions (closures)


SurrealQL Syntax

```
LET $parameter = |@parameters| @expression;
```

One powerful feature available in SurrealDB is the ability to define anonymous functions. These functions can be used to encapsulate reusable logic and can be called from within your queries. Below are some examples demonstrating their capabilities:

## Basic function definitions


```
-- Define an anonymous function that doubles a numberLET $double = |$n: number| $n * 2;RETURN $double(2);  -- Returns 4-- Define a function that concatenates two stringsLET $concat = |$a: string, $b: string| $a + $b;RETURN $concat("Hello, ", "World!");  -- Returns "Hello, World!"
```

```
-- Define a function that greets a personLET $greet = |$name: string| -> string { "Hello, " + $name + "!" };RETURN $greet("Alice");   -- Returns "Hello, Alice!"
```

## Error Handling and Type Enforcement


You can also enforce type constraints within your functions to prevent type mismatches:

```
-- Define a function with a return typeLET $to_upper = |$text: string| -> string { string::uppercase($text) };RETURN $to_upper("hello");  -- Returns "HELLO"RETURN $to_upper(123);      -- Error: type mismatch-- Define a function that accepts only numbersLET $square = |$num: number| $num * $num;RETURN $square(4);    -- Returns 16RETURN $square("4");  -- Error: type mismatch
```

## Closures in functions


Many of SurrealDB's functions allow a closure to be passed in, making it easy to use complex logic on a value or the elements of an array.

The `chain` function which performs an operation on a value before passing it on:

```
"Two"    .replace("Two", "2")    .chain(|$num| <number>$num * 1000);
```

Response

```
2000
```

We can see that the input to the `.chain()` method is indeed a closure by creating our own that is assigned to a parameter. This closure can be passed into `.chain()`, returning the same output as above.

```
LET $my_func = |$num| <number>$num * 1000;"Two"    .replace("Two", "2")    .chain($my_func);
```

The following example shows a chain of array functions used to remove useless data, followed by a check to see if all items in the array match a certain condition, and then a cast into another type. The array::filter call in the middle ensures that the string::len function that follows is being called on string values.

```
[NONE, NONE, "good data", "Also good", "important", NULL]    .filter(|$v| $v.is_string())    .all(|$s| $s.len() > 5)    .chain(|$v| <string>$v);
```

Response

```
'true'
```

## Closure limitations


Closures work inside a read-only context, and cannot be used to modify database resources.

```
-- 1. Create a test table and functionDEFINE TABLE test_table SCHEMAFULL;DEFINE FIELD name ON test_table TYPE string;DEFINE FUNCTION fn::test_create($name: string) -> object {    CREATE test_table CONTENT { name: $name };    { created: true, name: $name };};-- 2. Call the function directly - worksfn::test_create("direct_call");-- 3. Call the function inside .map() - failsLET $names = ["Alice", "Bob", "Charlie"];$names.map(|$n| fn::test_create($n));-- Error: "Couldn't write to a read only transaction"
```

In many cases, a closure can be substituted by another operation such as a `FOR` loop or a regular `SELECT` statement.

```
DEFINE TABLE test_table SCHEMAFULL;DEFINE FIELD name ON test_table TYPE string;DEFINE FUNCTION fn::test_create($name: string) -> object {    CREATE test_table CONTENT { name: $name };    { created: true, name: $name };};-- Function to create a record called for each nameSELECT VALUE fn::test_create($this) FROM ["Alice", "Bob", "Charlie"];
```

## Capturing parameters


The original implementation of closures did not allow them to capture parameters (variables) in their scope. Strictly speaking, this made them simple anonymous functions as closures did not "enclose" anything.

```
LET $okay_nums = [1,2,3];-- Returns [] because $okay_nums not present inside the closure[1,5,6,7,0].filter(|$n| $n IN $okay_nums);
```

This has since been resolved, allowing a parameter declared outside a closure to be recognized inside it.

```
LET $okay_nums = [1,2,3];[1,5,6,7,0].filter(|$n| $n IN $okay_nums);
```

## Conclusion


These anonymous functions provide a flexible way to define small, reusable pieces of logic that can be used throughout your queries. By leveraging them, you can write more modular and maintainable SurrealQL code.
