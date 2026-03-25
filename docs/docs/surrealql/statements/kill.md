---
title: KILL statement
url: https://surrealdb.com/docs/surrealql/statements/kill
crawled_at: 2026-03-25 18:41:19
---

# KILL statement


The `KILL` statement is used to terminate a running live query.

While the `KILL` statement does accept a value type, this value must resolve to a UUID. Consequently, it will accept a string literal of a UUID or a param.

### Statement syntax

SurrealQL SyntaxRailroad Diagram
SurrealQL Syntax

```
KILL @value;
```
KILL@value;
## Example usage


### Basic usage


The `KILL` statement expects the UUID of a running live select query to be passed. This UUID can be found in the output of the `LIVE` statement, and can thereafter be passed into a `KILL` statement once it is no longer needed.

```
LIVE SELECT DIFF FROM person;-- output: u'0189d6e3-8eac-703a-9a48-d9faa78b44b9'-- Some time later...KILL u"0189d6e3-8eac-703a-9a48-d9faa78b44b9";
```

The `KILL` statement also allows for parameters to be used.

```
-- Define the parameterLET $live_query_id = u"0189d6e3-8eac-703a-9a48-d9faa78b44b9";-- Use the parameterKILL $live_query_id;
```

Using the `KILL` statement on a UUID that does not correspond to a running live query will generate an error.

```
LET $rand = rand::uuid();KILL $rand;KILL u'9276b05b-e59a-49cd-9dd1-17c6fd15c28f';
```

Output

```
"Can not execute KILL statement using id '$rand'""Can not execute KILL statement using id 'u'9276b05b-e59a-49cd-9dd1-17c6fd15c28f''"
```

## Kill notifications


A separate notification is sent out when a `KILL` statement is enacted on a live query ID.

```
LIVE SELECT * FROM person;-- Output is a UUID:-- u'cf447091-9463-4d75-b32a-08513eb2a07c'KILL u'cf447091-9463-4d75-b32a-08513eb2a07c';
```

Output

```
-- Query 1NONE-- Notification (action: Killed, live query ID: cf447091-9463-4d75-b32a-08513eb2a07c)NONE
```
