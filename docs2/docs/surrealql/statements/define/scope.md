---
title: DEFINE SCOPE statement
url: https://surrealdb.com/docs/surrealql/statements/define/scope
crawled_at: 2026-03-25 19:08:32
---

###### Warning

This statement was deprecated in favour of `DEFINE ACCESS ... TYPE RECORD` in SurrealDB versions 2.x, and has been removed as of SurrealDB 3.0. Learn more in the [DEFINE ACCESS.

# `DEFINE SCOPE` statement

Setting scope access allows SurrealDB to operate as a web database. With scopes you can set authentication and access rules which enable fine-grained access to tables and fields.

## Requirements

- 
You must be authenticated as a root or namespace user before you can use the `DEFINE SCOPE` statement.

- 
[You must select your namespace and database before you can use the `DEFINE SCOPE` statement.


## Statement syntax

SurrealQL Syntax

```DEFINE SCOPE [ OVERWRITE | IF NOT EXISTS ] @name SESSION @duration SIGNUP @expression SIGNIN @expression [ COMMENT @string ]

```

## Example usage

Below shows how you can create a scope using the `DEFINE SCOPE` statement.

```-- Enable scope authentication directly in SurrealDB
DEFINE SCOPE account SESSION 24h
	SIGNUP ( CREATE user SET email = $email, pass = crypto::argon2::generate($pass) )
	SIGNIN ( SELECT * FROM user WHERE email = $email AND crypto::argon2::compare(pass, $pass) )
;

```

## Using `IF NOT EXISTS` clause

The `IF NOT EXISTS` clause can be used to define a scope only if it does not already exist. If the scope already exists, the `DEFINE SCOPE` statement will return an error.

```-- Create a SCOPE if it does not already exist
DEFINE SCOPE IF NOT EXISTS example;

```
