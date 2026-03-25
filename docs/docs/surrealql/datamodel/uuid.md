---
title: UUIDs
url: https://surrealdb.com/docs/surrealql/datamodel/uuid
crawled_at: 2026-03-25 18:40:43
---

# UUIDs


UUIDs represent UUID v4 and v7 values. They can be obtained via either the:

- rand::uuid::* functions
- casted from strings
- or via string prefixes

###### Note


As of `v2.0.0`, SurrealDB no longer eagerly converts a string into a UUID. An implicit `u` prefix or cast using `<uuid>` is required instead.

```
rand::uuid::v4();rand::uuid::v7();<uuid> "a8f30d8b-db67-47ec-8b38-ef703e05ad1b";u"a8f30d8b-db67-47ec-8b38-ef703e05ad1b";
```
