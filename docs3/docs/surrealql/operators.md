---
title: Operators
url: https://surrealdb.com/docs/surrealql/operators
crawled_at: 2026-03-25 21:39:55
---

# Operators


A variety of operators in SurrealQL allow for complex manipulation of data, and advanced logic.

| Operator | Description |
| --- | --- |
| && AND | Checks whether both of two values are truthy |
| || OR | Checks whether either of two values is truthy |
| ! | Reverses the truthiness of a value |
| !! | Determines the truthiness of a value |
| ?? | Check whether either of two values are truthy and not NULL |
| ?: | Check whether either of two values are truthy |
| = IS | Check whether two values are equal |
| != IS NOT | Check whether two values are not equal |
| == | Check whether two values are exactly equal |
| ?= | Check whether any value in a set is equal to a value |
| *= | Check whether all values in a set are equal to a value |
| ~ | Compare two values for equality using fuzzy matching |
| !~ | Compare two values for inequality using fuzzy matching |
| ?~ | Check whether any value in a set is equal to a value using fuzzy matching |
| *~ | Check whether all values in a set are equal to a value using fuzzy matching |
| < | Check whether a value is less than another value |
| <= | Check whether a value is less than or equal to another value |
| > | Check whether a value is greater than another value |
| >= | Check whether a value is greater than or equal to another value |
| + | Add two values together |
| - | Subtract a value from another value |
| * × | Multiply two values together |
| / ÷ | Divide a value by another value |
| ** | Raises a base value by another value |
| CONTAINS ∋ | Checks whether a value contains another value |
| CONTAINSNOT ∌ | Checks whether a value does not contain another value |
| CONTAINSALL ⊇ | Checks whether a value contains all other values |
| CONTAINSANY ⊃ | Checks whether a value contains any other value |
| CONTAINSNONE ⊅ | Checks whether a value contains none of the following values |
| INSIDE IN ∈ | Checks whether a value is contained within another value |
| NOTINSIDE NOT IN ∉ | Checks whether a value is not contained within another value |
| ALLINSIDE ⊆ | Checks whether all values are contained within other values |
| ANYINSIDE ⊂ | Checks whether any value is contained within other values |
| NONEINSIDE ⊄ | Checks whether no value is contained within other values |
| OUTSIDE | Checks whether a geometry type is outside of another geometry type |
| INTERSECTS | Checks whether a geometry type intersects another geometry type |
| @@ @[ref]@ | Checks whether the terms are found in a full-text indexed field |
| <|4|> <|3,HAMMING| > | Performs a K-Nearest Neighbors (KNN) search to find a specified number of records closest to a given data point, optionally using a defined distance metric. Supports customizing the number of results and choice of distance calculation method. |


## && or AND


The `and` operator checks whether both of two values are [truthy](/docs/surrealql/datamodel/values#values-and-truthiness).

```
SELECT * FROM 10 AND 20 AND 30;

-- 30

```


## || or OR


The `or` operator checks whether either of two values are [truthy](/docs/surrealql/datamodel/values#values-and-truthiness).

```
SELECT * FROM 0 OR false OR 10;

-- 10

```


## !


The `not` operator reverses the truthiness of a value.

```
SELECT * FROM !(TRUE OR FALSE);
-- false

SELECT * FROM !"Has a value";
-- false

```


## !!


The `not not` operator is simply an application of the `!` operator twice. It can be used to determines the truthiness of a value.

```
SELECT * FROM !!"Has a value";
-- true

```

## ??


The `null coalescing operator` checks whether either of two values are [truthy](/docs/surrealql/datamodel/values#values-and-truthiness) and not `NONE` or `NULL`.

```
SELECT * FROM NULL ?? 0 ?? false ?? 10;

-- 0

```


## ?:


The `truthy coalescing operator` checks whether either of two values are [truthy](/docs/surrealql/datamodel/values#values-and-truthiness).

```
SELECT * FROM NULL ?: 0 ?: false ?: 10;

-- 10

```


## = or IS


The `equal` operator checks whether two values are equal.

```
SELECT * FROM true = "true";
-- false

```

```
SELECT * FROM 10 = "10";
-- false

```

```
SELECT * FROM 10 = 10.00;
-- true

```

```
SELECT * FROM 10 = "10.3";
-- false

```

```
SELECT * FROM [1, 2, 3] = [1, 2, 3];
-- true

```

```
SELECT * FROM [1, 2, 3] = [1, 2, 3, 4];
-- false

```

```
SELECT * FROM { this: "object" } = { this: "object" };
-- true

```

```
SELECT * FROM { this: "object" } = { another: "object" };
-- false

```


## != or IS NOT


The `not equal` operator checks whether two values are not equal.

```
SELECT * FROM 10 != "15";
-- true

```

```
SELECT * FROM 10 != "test";
-- true

```

```
SELECT * FROM [1, 2, 3] != [3, 4, 5];
-- true

```


## ==


The `exact` operator checks whether two values are exact. This operator also checks that each value has the same type.

```
SELECT * FROM 10 == 10;
-- true

```

```
SELECT * FROM 10 == "10";
-- false

```

```
SELECT * FROM true == "true";
-- false

```


## ?=


The `any equal` operator checks whether any value in an array equals another value.

```
SELECT * FROM [10, 15, 20] ?= 10;
-- true

```


## *=


The `all equal` operator checks whether all values in an array equals another value.

```
SELECT * FROM [10, 10, 10] *= 10;
-- true

```


## ~ ?~ !~ *~


These operators used to compare two values for equality using fuzzy matching. They have been removed since 3.0 to avoid implicitly preferring one algorithm over another, as the type of fuzzy matching to use will depend on each individual case.

Please use the `string::similarity::*` functions instead:

```
let $threshold = 10;

string::similarity::smithwaterman("test text", "Test") > $threshold;
-- true

```


## <


The `less than` operator checks whether a value is less than another value.

```
SELECT * FROM 10 < 15;
-- true

```


## <=


The `less than or equal` operator checks whether a value is less than or equal to another value.

```
SELECT * FROM 10 <= 15;
-- true

```


## >


The `greater than` operator checks whether a value is less than another value.

```
SELECT * FROM 15 > 10;
-- true

```


## >=


The `greater than or equal` operator checks whether a value is less than or equal to another value.

```
SELECT * FROM 15 >= 10;
-- true

```


## +


The `add` operator adds two values together.

```
SELECT * FROM 10 + 10;
-- 20

```

```
SELECT * FROM "test" + " " + "this";
-- "test this"

```

```
SELECT * FROM 13h + 30m;
-- "13h30m"

```


## -


The `subtract` operator subtracts a value from another value.

```
SELECT * FROM 20 - 10;
-- 10

```

```
SELECT * FROM 2m - 1m;
-- 1m

```


## * or ×


The `multiply` operator multiplies a value by another value.

```
SELECT * FROM 20 * 2;
-- 40

```


## / or ÷


The `divide` operator divides a value by another value.

```
SELECT * FROM 20 / 2;
-- 10

```


## **


The `power` operator raises a base value by another value.

```
SELECT * FROM 20 ** 3;
-- 8000

```


## CONTAINS or ∋


The `contains` operator checks whether a value contains another value.

```
SELECT * FROM [10, 20, 30] CONTAINS 10;
-- true

```

```
SELECT * FROM "this is some text" CONTAINS "text";
-- true

```

```
SELECT * FROM {
	type: "Polygon",
	coordinates: [[
		[-0.38314819, 51.37692386], [0.1785278, 51.37692386],
		[0.1785278, 51.61460570], [-0.38314819, 51.61460570],
		[-0.38314819, 51.37692386]
	]]
} CONTAINS (-0.118092, 51.509865);

-- true

```


## CONTAINSNOT or ∌


The `not contains` operator checks whether a value does not contain another value.

```
SELECT * FROM [10, 20, 30] CONTAINSNOT 15;
-- true

```

```
SELECT * FROM "this is some text" CONTAINSNOT "other";
-- true

```

```
SELECT * FROM {
	type: "Polygon",
	coordinates: [[
		[-0.38314819, 51.37692386], [0.1785278, 51.37692386],
		[0.1785278, 51.61460570], [-0.38314819, 51.61460570],
		[-0.38314819, 51.37692386]
	]]
} CONTAINSNOT (-0.518092, 53.509865);

-- true

```


## CONTAINSALL or ⊇


The `contains all` operator checks whether a value contains all of multiple values.

```
SELECT * FROM [10, 20, 30] CONTAINSALL [10, 20, 10];
-- true

```


## CONTAINSANY or ⊃


The `contains any` operator checks whether a value contains any of multiple values.

```
SELECT * FROM [10, 20, 30] CONTAINSANY [10, 15, 25];
-- true

```


## INSIDE or ∈ or IN


The `inside` operator checks whether a value is contained within another value.

```
SELECT * FROM 10 INSIDE [10, 20, 30];
-- true

```

```
SELECT * FROM "text" INSIDE "this is some text";
-- true

```

```
SELECT * FROM (-0.118092, 51.509865) INSIDE {
	type: "Polygon",
	coordinates: [[
		[-0.38314819, 51.37692386], [0.1785278, 51.37692386],
		[0.1785278, 51.61460570], [-0.38314819, 51.61460570],
		[-0.38314819, 51.37692386]
	]]
};

true

```

This operator can also be used to check for the existence of a key inside an [object](/docs/surrealql/datamodel/objects). To do so, precede `IN` with the field name as a string.

```
"name" IN {
    name: "Riga",
    country: "Latvia"
};

-- true

```

`IN` can also be used with a record ID as long as the ID is expanded to include the fields. Both of the following queries will return `true`.

```
CREATE city:riga SET name = "Riga", country = "Latvia", population = 605273;

"name" IN city:riga.*;
"name" IN city:riga.{ name, country };

```


## NOTINSIDE or ∉ or NOT IN


The `not inside` operator checks whether a value is not contained within another value.

```
SELECT * FROM 15 NOTINSIDE [10, 20, 30];
-- true

```

```
SELECT * FROM "other" NOTINSIDE "this is some text";
-- true

```

```
SELECT * FROM (-0.518092, 53.509865) NOTINSIDE {
	type: "Polygon",
	coordinates: [[
		[-0.38314819, 51.37692386], [0.1785278, 51.37692386],
		[0.1785278, 51.61460570], [-0.38314819, 51.61460570],
		[-0.38314819, 51.37692386]
	]]
};

-- true

```


## ALLINSIDE or ⊆


The `all inside` operator checks whether all of multiple values are contained within another value.

```
SELECT * FROM [10, 20, 10] ALLINSIDE [10, 20, 30];
-- true

```


## ANYINSIDE or ⊂


The `any inside` operator checks whether any of multiple values are contained within another value.

```
SELECT * FROM [10, 15, 25] ANYINSIDE [10, 20, 30];
-- true

```


## NONEINSIDE or ⊄


The `none inside` operator checks whether none of multiple values are contained within another value.

```
SELECT * FROM [15, 25, 35] NONEINSIDE [10, 20, 30];
-- true

```


## OUTSIDE


The `outside` operator checks whether a geometry value is outside another geometry value.

```
SELECT * FROM (-0.518092, 53.509865) OUTSIDE {
	type: "Polygon",
	coordinates: [[
		[-0.38314819, 51.37692386], [0.1785278, 51.37692386],
		[0.1785278, 51.61460570], [-0.38314819, 51.61460570],
		[-0.38314819, 51.37692386]
	]]
};

-- true

```


## INTERSECTS


The `intersects` operator checks whether a geometry value intersects another geometry value.

```
SELECT * FROM {
	type: "Polygon",
	coordinates: [[
		[-0.38314819, 51.37692386], [0.1785278, 51.37692386],
		[0.1785278, 51.61460570], [-0.38314819, 51.61460570],
		[-0.38314819, 51.37692386]
	]]
} INTERSECTS {
	type: "Polygon",
	coordinates: [[
		[-0.11123657, 51.53160074], [-0.16925811, 51.51921169],
		[-0.11466979, 51.48223813], [-0.07381439, 51.51322956],
		[-0.11123657, 51.53160074]
	]]
};

-- true

```


## MATCHES


The `matches` operator checks whether the terms are found in a full-text indexed field.

```
SELECT * FROM book WHERE title @@ 'rust web';


[
	{
		id: book:1,
		title: 'Rust Web Programming'
	}
]

```

Using the matches operator with a reference checks whether the terms are found, highlights the searched terms, and computes the full-text score.

```
SELECT id,
		search::highlight('<b>', '</b>', 1) AS title,
		search::score(1) AS score
FROM book
WHERE title @1@ 'rust web'
ORDER BY score DESC;

[
	{
		id: book:1,
		score: 0.9227996468544006f,
		title: '<b>Rust</b> <b>Web</b> Programming'
	}
]

```

### AND, OR, and numeric operators inside @@


In addition to the `AND` keyword, the `OR` matches operator can also be used as of 3.0.0-beta. This allows a single string to be compared against instead of needing to specify individual parts of the string.

```
CREATE document:1 SET text = "It is rare that I find myself penning a personal note in my chronicles.";
DEFINE ANALYZER simple TOKENIZERS blank,class FILTERS lowercase;
DEFINE INDEX some_index ON document FIELDS text FULLTEXT ANALYZER simple;

-- @AND@ and @OR@: can use the entire string
SELECT * FROM document WHERE text @AND@ "personal rare";
SELECT * FROM document WHERE text @OR@ "personal nice weather today";

-- Separate AND and OR outside of matches operator:
-- Must specify parts of string to check for match
SELECT * FROM document WHERE text @@ "personal" AND text @@ "rare";
SELECT * FROM document WHERE text @@ "personal note";
SELECT * FROM document WHERE text @@ "personal" OR text @@ "nice weather today";

```

## KNN


K-Nearest Neighbors (KNN) is a fundamental algorithm used for classifying or regressing based on the closest data points in the feature space, with its performance and scalability critical in applications involving large datasets.

In practice, the efficiency and scalability of the KNN algorithm are crucial, especially when dealing with large datasets. Different implementations of KNN are tailored to optimize these aspects without compromising the accuracy of the results.

SurrealDB supports different K-Nearest Neighbors methods to perform KNN searches, each with unique requirements for syntax.
Below are the details for each method, including how to format your query with examples:

### Brute Force Method


Best for smaller datasets or when the highest accuracy is required.

SurrealQL Syntax

```
<|K,DISTANCE_METRIC|>

```

- K: The number of nearest neighbors to retrieve.
- DISTANCE_METRIC: The metric used to calculate distances, such as EUCLIDEAN or MANHATTAN.

```
CREATE pts:3 SET point = [8,9,10,11];
SELECT id FROM pts WHERE point <|2,EUCLIDEAN|> [2,3,4,5];

```

### HNSW Method


Recommended for very large datasets where speed is essential and some loss of accuracy is acceptable.

SurrealQL Syntax

```
<|K,EF|>

```

- K: The number of nearest neighbors.
- EF: The size of the dynamic candidate list during the search, affecting the search's accuracy and speed.

```
CREATE pts:3 SET point = [8,9,10,11];
DEFINE INDEX mt_pts ON pts FIELDS point HNSW DIMENSION 4 DIST EUCLIDEAN EFC 150 M 12;
SELECT id FROM pts WHERE point <|10,40|> [2,3,4,5];

```


## Using the ANY/ALL operators for string indexes


An index defined on a string value can be used via the operators `CONTAINSANY`, `ALLINSIDE`, or `ANYINSIDE`. The operator `CONTAINS`, however, will not use a defined index as `CONTAINS` is used for substring matches between strings themselves as opposed to an index lookup.

```
DEFINE FIELD name ON account TYPE string;
DEFINE INDEX name_index ON account FIELDS name;

CREATE account:billy SET name = "Billy McConnell";

-- Both return the user Billy McConnell
SELECT * FROM account WHERE name CONTAINS "Billy McConnell";
SELECT * FROM account WHERE name CONTAINSANY ["Billy McConnell"];

-- However, CONTAINS does not use the index
SELECT * FROM account WHERE name CONTAINS "Billy McConnell" EXPLAIN FULL;
-- CONTAINSANY + putting the value inside an array will use the index
SELECT * FROM account WHERE name CONTAINSANY ["Billy McConnell"] EXPLAIN FULL;

```

## Types of operators, order of operations and binding power


To determine which operator is executed first, a concept called "binding power" is used. Operators with greater binding power will operate directly on their neighbours before those with lower binding power. The following is a list of all operator types from greatest to lowest binding power.

| Operator name | Description |
| --- | --- |
| Unary | The Unary operators are !, +, and -. |
| Nullish | The Nullish operators are ?: and ??. |
| Range | The Range operator is ... |
| Cast | The Cast operator is `, with type_name a stand in for the type to cast into. For example, or `. |
| Power | The only Power operator is **. |
| MulDiv | The MulDiv (multiplication and division) operators are *, /, ÷, and %. |
| AddSub | The AddSub (addition and subtraction) operators are + and -. |
| Relation | The Relation operators are `=, ∋, CONTAINS, ∌, CONTAINSNOT, ∈, INSIDE, ∉, NOTINSIDE, ⊇, CONTAINSALL, ⊃, CONTAINSANY, ⊅, CONTAINSNONE, ⊆, ALLINSIDE, ⊂, ANYINSIDE, ⊄, NONEINSIDE, OUTSIDE, INTERSECTS, NOT, and IN`. |
| Equality | The Equality operators are =, IS, ==, !=, *=, ?=, and @. |
| And | The And operators are && and AND. |
| Or | The Or operators are || and OR. |


## Examples of binding power


The following samples show examples of basic operations of varying binding power. The original example is followed by the same example with the parts with higher binding power in parentheses, then the final expression after the first bound portion is calculated, and finally the output.

MulDiv first, then AddSub

```
1 + 3 * 4;
1 + (3 * 4);
-- Final expression
1 + 12;
-- Output
13

```

Power first, then MulDiv

```
2**3 * 3;
(2**3) * 3;
-- Final expression
8*3;
-- Output
24

```

Unary first, then cast

```
<string>-4;
<string>(-4);
-- Output
"-4"

```

Cast first, then Power

```
<number>"9"**9;
(<number>"9")**9;
-- Final expression
9**9;
-- Output
387420489

```

AddSub first, then Relation

```
"c" + "at" IN "cats";
("c" + "at") IN "cats";
-- Final expression
"cat" IN "cats";
-- Output
true

```

And first, then Or

```
true AND false OR true;
(true AND false) OR true;
-- Final expression
false OR true;
-- Output
true

```

Unary, then Cast, then Power, then AddSub

```
<decimal>-4**2+4;
((<decimal>(-4))**2)+4;
-- Output
20dec

```
