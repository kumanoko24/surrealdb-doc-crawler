---
title: SPLIT clause
url: https://surrealdb.com/docs/surrealql/clauses/split
crawled_at: 2026-03-25 18:41:56
---

# SPLIT clause


The `SPLIT` clause in SurrealQL is used to split the results of a query based on a specific field, particularly when dealing with arrays. This is useful in scenarios where you want to treat each element of an array as a separate row in the result set. It can be particularly helpful in data analysis contexts where you need to work with individual elements of an array separately.

## Syntax


Clause Syntax

```
SPLIT [ON] @field
```

Suppose you have a user table with a field emails that contains an array of email addresses for each user. You want to list each email address as a separate record.

Here's how you can use the SPLIT clause in SurrealQL:

```
CREATE user SET    name = "John Doe",    emails = ["john@example.com", "doe@example.com"];-- Split the results by each value in the emails arraySELECT * FROM user SPLIT emails;
```

Explanation:

- CREATE user SET ...: This creates a user record with a name and an array of email addresses.
- SELECT * FROM user SPLIT emails: This query selects all fields from the user table and splits the results based on the emails field. Each email address in the emails array will now be in a field of the same name that only contains a single value.

Output:
The output of the query will be:

```
[	{		emails: 'john@example.com',		id: user:unjgil312jvvxfbdj706,		name: 'John Doe'	},	{		emails: 'doe@example.com',		id: user:unjgil312jvvxfbdj706,		name: 'John Doe'	}]
```

## Using SPLIT to restructure collected paths


One practical use case with `SPLIT` is returning every possible combination of the relations inside multiple graph paths. For instance, take the following data below that represents the relations between Canada the country, its provinces, and their cities.

```
CREATE country:canada;CREATE province:bc, province:alberta;CREATE city:vancouver, city:victoria, city:edmonton, city:calgary;RELATE [city:vancouver, city:victoria]->in->province:bc;RELATE [city:edmonton, city:calgary]->in->province:alberta;RELATE [province:bc, province:alberta]->in->country:canada;
```

A graph query on both of these paths shows all of the provinces and cities.

```
SELECT     id AS country,    <-in<-province AS provinces,    <-in<-province<-in<-city AS cities FROM ONLY country:canada;
```

Output

```
{	cities: [		city:calgary,		city:edmonton,		city:vancouver,		city:victoria	],	country: country:canada,	provinces: [		province:alberta,		province:bc	]}
```

Using `SPLIT` in this case transforms the output from a collection of paths centred on the `country:canada` record into an array of objects, each representing every possible combination of cities and provinces inside the country.

```
SELECT    id AS country,    <-in<-province AS province,    <-in<-province<-in<-city AS city FROM country:canada    SPLIT city, province;
```

Output

```
[	{		city: city:calgary,		country: country:canada,		province: province:alberta	},	{		city: city:calgary,		country: country:canada,		province: province:bc	},	{		city: city:edmonton,		country: country:canada,		province: province:alberta	},	{		city: city:edmonton,		country: country:canada,		province: province:bc	},	{		city: city:vancouver,		country: country:canada,		province: province:alberta	},	{		city: city:vancouver,		country: country:canada,		province: province:bc	},	{		city: city:victoria,		country: country:canada,		province: province:alberta	},	{		city: city:victoria,		country: country:canada,		province: province:bc	}]
```

An example of the same query then mapped into a set of unique keys for serialization:

```
(SELECT    id,    <-in<-province AS province,    <-in<-province<-in<-city AS city FROM country:canada    SPLIT city, province).map(|$obj|     <string>$obj.id.id()     + '|'     + <string>$obj.province.id()     + '|'     + <string>$obj.city.id());
```

Output

```
[	'canada|alberta|calgary',	'canada|bc|calgary',	'canada|alberta|edmonton',	'canada|bc|edmonton',	'canada|alberta|vancouver',	'canada|bc|vancouver',	'canada|alberta|victoria',	'canada|bc|victoria']
```
