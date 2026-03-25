---
title: Data types
url: https://surrealdb.com/docs/surrealql/datamodel
crawled_at: 2026-03-25 18:40:18
---

# Data types


SurrealQL allows you to describe data with specific data types. These data types are used to validate data and to generate the appropriate database schema.

| Type | Description |
| --- | --- |
| any | Use this when you explicitly don't want to specify the field's data type. The field will allow any data type supported by SurrealDB. |
| array | An array of items.                 The array type also allows you to define which types can be stored in the array and the required length.                                      array                     array<string>                     array<string, 10> |
| bool | Describes whether something is truthy or not. |
| bytes | Stores a value in a byte array.                                      <bytes>value                     bytes |
| datetime | An RFC 3339 compliant data type that stores a date with time and time zone. |
| decimal | Data type for storing decimal floating point numbers. |
| duration | Store a value representing a length of time. Can be added or subtracted from datetimes or other durations. |
| float | Data type for storing floating point numbers. Larger or extremely precise values should be stored as a decimal. |
| geometry | RFC 7946 compliant data type for storing geometry in the GeoJson format.                                      geometry<feature>                     geometry<point>                     geometry<line>                     geometry<polygon>                     geometry<multipoint>                     geometry<multiline>                     geometry<multipolygon>                     geometry<collection> |
| int | Store a value in a 64 bit signed integer. Values can range between -9223372036854775808 and 9223372036854775807 (inclusive). Larger values should be stored as a float or a decimal. |
| number | Store numbers without specifying the type.                 SurrealDB will detect the type of number and store it using the minimal number of bytes. |
| object | Store formatted objects containing values of any supported type including nested objects or arrays. |
| regex | A compiled regular expression that can be used for matching strings. |
| literal | A value that may have multiple representations or formats, similar to an enum or a union type. Can be composed of strings, numbers, objects, arrays, or durations.                                      "a" | "b"                     [number, "abc"]                     123 | 456 | string | 1y1m1d |
| option | Makes types optional and guarantees the field to be either empty (NONE) or some other type.                                      option<number> |
| range | A range of possible values. Lower and upper bounds can be set, in the absence of which the range becomes open-ended. A range of integers can be used in a FOR loop.                                      0..10                      0..=10                      ..10                      'a'..'z' |
| record | Store a reference to another record. The value must be a Record ID. Add the record name inside angle brackets to restrict the reference to only certain record names.                                      record                     record<user>                     record<user | administrator> |
| set | A set of items.                 The set type also allows you to define which types can be stored in the set and the required length.                 Items are automatically deduplicated and orderd.                                      set                     set<string>                     set<string, 10> |
| string | Describes a text-like value. |


## Examples


### geometry


```
-- Define a field with a single typeDEFINE FIELD location ON TABLE restaurant TYPE geometry<point>;-- Define a field with any geometric typeDEFINE FIELD area ON TABLE restaurant TYPE geometry<feature>;-- Define a field with specific geometric typesDEFINE FIELD area ON TABLE restaurant TYPE geometry<polygon|multipolygon|collection>;
```

### bytes


```
-- Define a field with a single typeDEFINE FIELD image ON TABLE product TYPE bytes;-- Create a record with a bytes field and set the valueCREATE foo SET value = <bytes>"bar";
```
