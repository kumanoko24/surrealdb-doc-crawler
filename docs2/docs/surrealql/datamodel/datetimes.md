---
title: Datetimes
url: https://surrealdb.com/docs/surrealql/datamodel/datetimes
crawled_at: 2026-03-25 19:08:58
---

# Datetimes

SurrealDB has native support for datetimes with nanosecond precision. SurrealDB automatically parses and understands datetimes which are written as strings in the SurrealQL language. Times must also be formatted in [RFC 3339 format.

Datetimes are represented and created by a `d` prefex in front of a string.

```CREATE event SET time = d"2025-07-03T07:18:52Z";

```

SurrealDB handles all datetimes with nanosecond precision.

```CREATE event SET time = d"2025-07-03T07:18:52.841147Z";

```

SurrealDB handles all timezones, and automatically converts and stores datetimes as a UTC date.

```CREATE event SET time = d"2025-07-03T07:18:52.841147+02:00";

```

A `datetime` can also be created by using `<datetime>` to cast from a string.

With correct input:

```CREATE event SET time = <datetime>"2025-07-03T07:18:52.841147Z";

```

Response

```[{ id: event:jwm8ncmfi30nrxdf24ws, time: d'2025-07-03T07:18:52.841147Z' }]

```

With incorrect input (missing final Z):

```CREATE event SET time = <datetime>"2025-07-03T07:18:52.841147";

```

Response

```"Expected a datetime but cannot convert '2025-07-03T07:18:52.841147' into a datetime"

```

As a convenience, a date containing a year, month and day but no time will also parse correctly as a datetime.

```CREATE event SET time = <datetime>"2024-04-03";

```

Response

```[{ id: event:4t50wjjlne9v8km2qcwq, time: d'2024-04-03T00:00:00Z' }]

```

## Datetime types in `DEFINE FIELD` statements

Defining a field with a set `datetime` type will ensure that datetimes are properly formatted and not passed on as simple strings.

```DEFINE FIELD time ON event TYPE datetime;
CREATE event SET time = "2025-07-03T07:18:52.841147";

```

Response

```"Couldn't coerce value for field `time` of `event:qv8qcjf0w9oowekl36w6`: Expected `datetime` but found `'2025-07-03T07:18:52.841147'`"

```

The above query will fail because the datetime is not cast as a datetime type. The correct query is:

```DEFINE FIELD time ON event TYPE datetime;
CREATE event SET time = d"2025-07-03T07:18:52.84114Z";

```

Response

```[
    { 
        id: event:w2lhv58f7c9z7xo4nqkq, 
        time: d'2025-07-03T07:18:52.841140Z' 
    }
]

```

### Datetime comparison

A datetime can be compared with another using the advanced SurrealDB operators.

```d"2025-07-03T07:18:52Z" < d"2025-07-03T07:18:52.84114Z";

```

Response

```true

```

## Durations and datetimes

A duration can be used to alter a datetime.

```CREATE event SET time = d"2025-07-03T07:18:52Z" + 2w;

```

Response

```[{ id: event:`9ey7v8r0fd46xblf9dsf`, time: d'2025-07-17T07:18:52Z' }]

```

Multi-part durations can also be used to modify datetimes.

```CREATE event SET time = d"2025-07-03T07:18:52.841147Z" + 1h30m20s1350ms;

```

Response

```[{ id: event:5uuzy32t48yutxyszi7p, time: d'2025-07-03T08:49:14.191147Z' }]

```

## Altering datetimes

Each value in a datetime can be set by using one of seven `time::set_` functions. Each of these function names ends with the part of the datetime that is modified, such as `time::set_year()` or `time::set_hour()`.

```d'1970-01-01T00:00:00.000000100Z'.set_year(1914);
-- Output
d'1914-01-01T00:00:00.000000100Z'

```

As these functions do not modify an existing datetime but return a new one, they can be chained one after another.

```d'1970-01-01T00:00:00.000000100Z'
    .set_year(1914)
    .set_month(6)
    .set_day(28);

-- Output
d'1914-06-28T00:00:00.000000100Z'

```

## Next steps

You've now seen how to store, modify, and handle dates and times in SurrealDB. For more advanced functionality, take a look at the [time functions, which enable extracting, altering, rounding, and grouping datetimes into specific time intervals.
