---
title: Casting
url: https://surrealdb.com/docs/surrealql/datamodel/casting
crawled_at: 2026-03-25 21:40:23
---

# Casting


In the SurrealDB type system, values can be converted to other values efficiently. This is useful if input is specified in a query which must be of a certain type, or if a user may have provided a parameter with an incorrect type.

| Type | Description |
| --- | --- |
| <array> | Casts the subsequent value into an array |
| <array<T>> | Casts the subsequent value into an array of T (some indicated type) |
| <bool> | Casts the subsequent value into a boolean |
| <datetime> | Casts the subsequent value into a datetime |
| <decimal> | Casts the subsequent value into a decimal |
| <duration> | Casts the subsequent value into a duration |
| <float> | Casts the subsequent value into a float |
| <int> | Casts the subsequent value into a int |
| <number> | Casts the subsequent value into a decimal |
| <record> | Casts the subsequent value into a record |
| <record<T>> | Casts the subsequent value into a record of T (some indicated type) |
| <set> | Casts the subsequent value into a set |
| <string> | Casts the subsequent value into a string |
| <regex> | Casts the subsequent value into a regular expression |
| <uuid> | Casts the subsequent value into a UUID |


## <array>


The `<array>` casting function converts a range into an array.

```
<array>1..=3;
-- Output:
[1, 2, 3]

```

## <array<T>>


The `<array<T>>` casting function converts a value into an array of the specified type.

###### Note


When using this casting function, the value must be an array and each element in the array will be cast to the specified type.

```
<array<int>>["42", "314", "271", "137", "141"];
-- Output:
[42, 314, 271, 137, 141]

```

```
<array<string>> [42, 314, 271, 137, 141];
-- Output:
['42', '314', '271', '137', '141']

```

A cast into an array of more than one possible type can also be used. In this case, the cast will attempt to cast into the possible types in order. As such, the `string` in the first query below will be cast into a `datetime` but not in the second.

```
[
  <array<datetime|string>>["2020-09-09", "21 Jan 2020"],
  <array<string|datetime>>["2020-09-09", "21 Jan 2020"]
];

```

Output

```
[
	[
		d'2020-09-09T00:00:00Z',
		'21 Jan 2020'
	],
	[
		'2020-09-09',
		'21 Jan 2020'
	]
]

```

An example of even more complex casting which attempts to cast each item in the input array into a `record<user>`, then `record<person>`, then `array<record<user>>`, and finally `string`.

```
<array<record<user | person> | array<record<user>> | string>> [
	'person:one',
	'user:two',
	[
		'user:three',
		'user:four'
	],
	'not_a_person_or_user'
];

```

Output

```
[
	person:one,
	user:two,
	[
		user:three,
		user:four
	],
	'not_a_person_or_user'
]

```

## <bool>


The `<bool` casting function converts a value into a boolean.

```
<bool>"true";
-- Output:
true

```

```
<bool>"false";
-- Output:
false

```

## <datetime>


The `<datetime>` casting function converts a value into a datetime.

```
<datetime>"2025-06-07";
-- Output:
d'2025-06-07T00:00:00Z'

```

## <decimal>


The `<decimal>` casting function converts a value into a decimal which allows for 128 bits of precision.

```
<decimal>"13.5729484672938472938410938456";
-- Output:
13.572948467293847293841093846dec

```

Decimal casting should generally not be used to convert from floats with a large number of digits after the decimal point, because the input to the right will first be turned into a less precise float before the cast is performed.

```
<decimal>13.572948467293847293841093845679289;
-- Output:
13.57294846729385dec

<decimal>1.193847193847193847193487E11;
-- Output:
119384719384.7194dec

```

In this case, the `dec` suffix is preferable as it will instruct the database to treat the **input** as a decimal, rather than create a float to then cast into a decimal.

```
13.572948467293847293841093845679289dec;
-- Output:
13.572948467293847293841093846dec

1.193847193847193847193487E11dec;
-- Output:
1.193847193847193847193487E11dec;

```

## <duration>


The `<duration>` casting function converts a value into a duration.

```
<duration>"1h30m";
-- Output:
1h30m

```


## <float>


The `<float>` casting function converts a value into a floating point number. Floating point numbers by nature have a limited amount of precision.

```
<float>13.572948467293847293841093845679289;
-- Output:
13.572948467293847f

```

```
<float>"13.572948467293847293841093845679289";
-- Output:
13.572948467293847

```

## <int>


The `<int>` casting function converts a value into an integer.

```
<int>53;
-- Output:
53

```

## <number>


The `<number>` casting function converts a value into a `number`.

```
<number>13.572948467293847293841093845679289;
-- Output:
"13.572948467293847293841093845679289"

```

```
<number>"13.572948467293847293841093845679289";
-- Output:
"13.572948467293847293841093845679289"

```

```
<number>1.193847193847193847193487E11;
-- Output:
"119384719384.7193847193487"

```

## <record>


The `<record>` casting function converts a value into a record.

Keep in mind when using this casting function that if the equivalent record id does not exist, it will not return anything.

```
SELECT id FROM <record>"person:hrebrffwm4sr2yifglta";

```

Output

```
{ id: person:hrebrffwm4sr2yifglta }

```

## <record<T>>


The `<record<T>>` casting function converts a value into a record.

Keep in mind when using this casting function that if the equivalent record id does not exist, it will not return anything.

```
SELECT id FROM <record>"person:hrebrffwm4sr2yifglta";
-- Output:
{ id: person:hrebrffwm4sr2yifglta }

```

A cast into a number of possible record types can also be used.

```
[
  <record<user|person>>"user:one",
  <array<record<user|person>>>["person:one", "user:two"]
];

```

Output

```
[
	user:one,
	[
		person:one,
		user:two
	]
]

```

## <set> and <set<T>>


The `<set>` casting function converts a value into a set.

```
[
  <set<datetime|string>>["2020-09-09", "21 Jan 2020"],
  <set<string|datetime>>["2020-09-09", "21 Jan 2020"]
];

```

Output

```
[
	[
		d'2020-09-09T00:00:00Z',
		'21 Jan 2020'
	],
	[
		'2020-09-09',
		'21 Jan 2020'
	]
]

```

## <string>


The `<string>` casting function converts a value into a string.

```
<string>true;
-- Output:
'true'

```

```
<string>1.3463;
-- Output:
'1.3463f'

```

```
<string>false;
-- Output:
"false"

```

## <regex>


The `<regex>` casting function converts a value into a regular expression.

```
<regex> "a|b" = "a";
-- Output:
true

```

```
<regex> "a|b" = "c";
-- Output:
false

```

## <uuid>


The `<uuid>` casting function converts a value into a UUID.

```
SELECT id FROM <uuid> "a8f30d8b-db67-47ec-8b38-ef703e05ad1b";
-- Output:
[ u'a8f30d8b-db67-47ec-8b38-ef703e05ad1b' ]

```

## General notes on casting


### Syntax and order


As the parser ignores spaces and new lines, casting syntax can include spaces or new lines as desired.

```
-- Surrealist formatted syntax
 <array<bool | string | float>> [
	'9.1',
	'true',
	15h
];

-- Maybe someone's preferred syntax?
<array
        <bool | string | float>
      >
[ '9.1', 'true', 15h ];

```

When more than one cast type is specified, SurrealDB will attempt to convert into the type in the order specified. In the example above, while the input `'9.1'` could have been converted to a float, the type `string` comes first in the cast syntax and thus `'9.1'` remains as a string.

Output

```
[
	'9.1',
	true,
	'15h'
]

```

### Casting vs. affixes


SurrealDB uses a number of affixes to force the parser to treat an input as a certain type instead of another. These affixes may seem at first glance to be identical to casts, as the following queries show.

```
-- All return a record person:one
r"person:one";
<record>"person:one";
<record<person>>"person:one";
-- Returns a string 'person:one'
'person:one';

-- Both return a decimal 98dec
98dec;
<decimal>98;

-- Returns an int 98
98;

```

However, casts and affixes work in different ways:

- A cast is a way to convert from one type into another.
- An affix is an instruction to the parser to treat an input as a certain type.

These differences become clear when working with input that is less than ideal or does not work with a certain type. For example, floats by nature become imprecise after a certain number of digits.

```
[
  8.888,
  8.8888888888888888
];

```

Output

```
[
	8.888f,
	8.88888888888889f
]

```

In this case, a `decimal` can be used which will allow a greater number of digits after the decimal point. However, casting the above numbers into a `decimal` will result in the same inaccurate output.

```
[
	<decimal>8.888,
	<decimal>8.888888888888888
];

```

Output

```
[
	8.888dec,
	8.88888888888889dec
]

```

This is because the parser will first treat the number as a float and then cast it into a `decimal`.

However, using the `dec` suffix will inform the parser that the entire input is to be treated as a `decimal` and it will never pass through a stage in which it is a float.

```
[
	8.888dec,
	8.888888888888888dec
];

```

Output

```
[
	8.888dec,
	8.888888888888888dec
]

```

Similarly, an attempt to cast a number that is too large for an `int` into a `decimal` will not work, as the parser will first attempt to handle the number on the right before moving on to the cast.

```
<decimal>9999999999999999999;

```

Output

```
'Failed to parse number: number cannot fit within a 64bit signed integer'

```

However, if the same number is followed by the `dec` suffix, the parser will be aware that the input is meant to be treated as a `decimal` from the outset and the query will succeed.

```
9999999999999999999dec;

```
