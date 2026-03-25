---
title: Parse functions
url: https://surrealdb.com/docs/surrealql/functions/database/parse
crawled_at: 2026-03-25 19:09:27
---

# Parse functions

These functions can be used when parsing email addresses and URL web addresses.


| Function |Description | |
| `parse::&#8203;email::host()` |Parses and returns an email host from an email address | |
| `parse::&#8203;email::user()` |Parses and returns an email username from an email address | |
| `parse::url::domain()` |Parses and returns the domain from a URL | |
| `parse::url::fragment()` |Parses and returns the fragment from a URL | |
| `parse::url::host()` |Parses and returns the hostname from a URL | |
| `parse::url::path()` |Parses and returns the path from a URL | |
| `parse::url::port()` |Parses and returns the port number from a URL | |
| `parse::url::scheme()` |Parses and returns the scheme from a URL | |
| `parse::url::query()` |Parses and returns the query string from a URL | |
## `parse::email::host`

The `parse::email::host` function parses and returns an email host from a valid email address.

API DEFINITION

```parse::email::host(string) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN parse::email::host("info@surrealdb.com");

-- 'surrealdb.com'

```


## `parse::email::user`

The `parse::email::user` function parses and returns an email username from a valid email address.

API DEFINITION

```parse::email::user(string) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN parse::email::user("info@surrealdb.com");

-- "info"

```


## `parse::url::domain`

The `parse::url::domain` function parses and returns domain from a valid URL. This function is similar to `parse::url::host` only that it will return `null` if the URL is an IP address.

API DEFINITION

```parse::url::domain(string) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN parse::url::domain("https://surrealdb.com:80/features?some=option#fragment");
RETURN parse::url::domain("http://127.0.0.1/index.html");

```

Response

```"surrealdb.com"

NONE

```


## `parse::url::fragment`

The `parse::url::fragment` function parses and returns the fragment from a valid URL.

API DEFINITION

```parse::url::fragment(string) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN parse::url::fragment("https://surrealdb.com:80/features?some=option#fragment");

-- 'fragment'

```


## `parse::url::host`

The `parse::url::host` function parses and returns the hostname from a valid URL.

API DEFINITION

```parse::url::host(string) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN parse::url::host("https://surrealdb.com:80/features?some=option#fragment");
RETURN parse::url::host("http://127.0.0.1/index.html");

```

Response

```'surrealdb.com'

'127.0.0.1'

```


## `parse::url::path`

The `parse::url::path` function parses and returns the path from a valid URL.

API DEFINITION

```parse::url::path(string) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN parse::url::path("https://surrealdb.com:80/features?some=option#fragment");

-- '/features'

```


## `parse::url::port`

The `parse::url::port` function parses and returns the port from a valid URL.

API DEFINITION

```parse::url::port(string) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN parse::url::port("https://surrealdb.com:80/features?some=option#fragment");

-- 80

```


## `parse::url::scheme`

The `parse::url::scheme` function parses and returns the scheme from a valid URL, in lowercase, as an ASCII string without the ':' delimiter.

API DEFINITION

```parse::url::scheme(string) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN parse::url::scheme("https://surrealdb.com:80/features?some=option#fragment");

-- 'https'

```


## `parse::url::query`

The `parse::url::query` function parses and returns the query from a valid URL.

API DEFINITION

```parse::url::query(string) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN parse::url::query("https://surrealdb.com:80/features?some=option#fragment");

-- 'some=option'

```
