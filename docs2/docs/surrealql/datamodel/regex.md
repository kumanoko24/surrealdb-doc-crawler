---
title: Regex
url: https://surrealdb.com/docs/surrealql/datamodel/regex
crawled_at: 2026-03-25 19:08:00
---

# Regex

A `regex` can be created by casting from a string.

The following examples all return `true`.

```-- Either 'a' or 'b'
<regex> "a|b" = "a";

-- Either color or colour
<regex> "col(o|ou)r" = "colour";

-- Case-insensitive match on English color, colour, or French couleur
<regex> "((?i)col(o|ou)r|couleur)" = "COULEUR";

```

While `regex` was added as a standalone type in version 2.3.0, regex matching has always been available via the [`string::matches()` function.

```string::matches("a", "a|b");
string::matches("colour", "col(o|ou)r");
string::matches("COULEUR", "((?i)col(o|ou)r|couleur)");

```
