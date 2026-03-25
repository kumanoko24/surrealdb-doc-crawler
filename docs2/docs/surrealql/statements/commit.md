---
title: COMMIT statement
url: https://surrealdb.com/docs/surrealql/statements/commit
crawled_at: 2026-03-25 19:08:51
---

# `COMMIT` statement

Each statement within SurrealDB is run within its own transaction by default. If a set of changes need to be made together, then groups of statements can be run together as a single transaction, either succeeding as a whole, or failing without leaving any residual data modifications. A `COMMIT` statement is used at the end of such a transaction to make the data modifications a permanent part of the database.

### Statement syntax

SurrealQL Syntax

```COMMIT [ TRANSACTION ];

```

## Example usage

The following query shows example usage of this statement.

```BEGIN TRANSACTION;

-- Setup accounts
CREATE account:one SET balance = 135605.16;
CREATE account:two SET balance = 91031.31;

-- Move money
UPDATE account:one SET balance += 300.00;
UPDATE account:two SET balance -= 300.00;

-- Finalise all changes
COMMIT TRANSACTION;

```

The following two options can be used at any point if a transaction must be cancelled without commiting the changes:

- 
[CANCEL to manually cancel the transaction.

- 
[THROW to cancel a transaction with an optional error message. THROW is the only way to cancel a transaction based on a condition, such as inside an [IF..ELSE block.


In addition, a `RETURN` statement can be used to return early from a successful transaction. This is often used in order to return a customized output.

```BEGIN;

CREATE account:one SET balance = 135605.16;
CREATE account:two SET balance = 91031.31, wants_to_send_money = true;

IF !account:two.wants_to_send_money {
    THROW "Customer doesn't want to send any money!";
};

LET $first = UPDATE ONLY account:one SET balance += 300.00;
LET $second = UPDATE ONLY account:two SET balance -= 300.00;

RETURN "Money sent! Status:\n" + <string>$first + '\n' + <string>$second;

COMMIT;

```

Output

```'Money sent! Status:
{ balance: 135905.16f, id: account:one }
{ balance: 90731.31f, id: account:two, wants_to_send_money: true }'

```
