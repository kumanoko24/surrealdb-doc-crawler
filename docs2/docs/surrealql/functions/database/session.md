---
title: Session functions
url: https://surrealdb.com/docs/surrealql/functions/database/session
crawled_at: 2026-03-25 19:08:43
---

# Session functions

These functions return information about the current SurrealDB session.


| Function |Description | |
| `session::ac()` |Returns the current user's access method | |
| `session::db()` |Returns the currently selected database | |
| `session::id()` |Returns the current user's session ID | |
| `session::ip()` |Returns the current user's session IP address | |
| `session::ns()` |Returns the currently selected namespace | |
| `session::origin()` |Returns the current user's HTTP origin | |
| `session::rd()` |Returns the current user's record authentication data | |
| `session::token()` |Returns the current user's authentication token | |
## `session::ac`

###### Note

This function was known as `session::sc` in versions of SurrrealDB before 2.0. The behaviour has not changed.

The `session::ac` function returns the current user's access method.

API DEFINITION

```session::ac() -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN session::ac();

"user"

```


## `session::db`

The `session::db` function returns the currently selected database.

API DEFINITION

```session::db() -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN session::db();

"my_db"

```


## `session::id`

The `session::id` function returns the current user's session ID.

API DEFINITION

```session::id() -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN session::id();

"I895rKuixHwCNIduyBIYH2M0Pga7oUmWnng5exEE4a7EB942GVElGrnRhE5scF5d"

```


## `session::ip`

The `session::ip` function returns the current user's session IP address.

API DEFINITION

```session::ip() -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN session::ip();

"2001:db8:3333:4444:CCCC:DDDD:EEEE:FFFF"

```


## `session::ns`

The `session::ns` function returns the currently selected namespace.

API DEFINITION

```session::ns() -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN session::ns();

"my_ns"

```


## `session::origin`

The `session::origin` function returns the current user's HTTP origin.

API DEFINITION

```session::origin() -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN session::origin();

"http://localhost:3000"

```


## `session::rd`

The `session::rd` function returns the current user's record authentication.

API DEFINITION

```session::rd() -> string

```

## `session::token`

The `session::token` function returns the current authentication token.

API DEFINITION

```session::token() -> string

```
