---
title: CANCEL statement
url: https://surrealdb.com/docs/surrealql/statements/cancel
crawled_at: 2026-03-25 18:41:03
---

# CANCEL statement


Each statement within SurrealDB is run within its own transaction. If a set of changes need to be made together, then groups of statements can be run together as a single transaction, either succeeding as a whole, or failing without leaving any residual data modifications. While a transaction will fail if any of its statements encounters an error, the `CANCEL` statement can also be used to cancel a transaction manually.

### Statement syntax

SurrealQL SyntaxRailroad Diagram
SurrealQL Syntax

```
CANCEL [ TRANSACTION ];
```
CANCELTRANSACTION;
## Example usage


The following query shows example usage of this statement.

```
BEGIN TRANSACTION;-- Setup accountsCREATE account:one SET balance = 135605.16;CREATE account:two SET balance = 91031.31;-- Move moneyUPDATE account:one SET balance += 300.00;UPDATE account:two SET balance -= 300.00;-- Rollback all changesCANCEL TRANSACTION;
```

`CANCEL` is not used to automatically cancel a transaction based on a condition such as inside an IF..ELSE block. Instead, a THROW statement is used. THROW can be followed by any value, usually a string containing context behind the error.

```
BEGIN TRANSACTION;-- Setup accountsCREATE account:one SET balance = 135605.16;CREATE account:two SET balance = 200.31;-- Move moneyUPDATE account:one SET balance += 300.00;UPDATE account:two SET balance -= 300.00;IF account:two.balance < 0 {    THROW "Not enough funds";};COMMIT TRANSACTION;
```
