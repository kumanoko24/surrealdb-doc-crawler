---
title: Duration functions
url: https://surrealdb.com/docs/surrealql/functions/database/duration
crawled_at: 2026-03-25 21:42:22
---

# Duration functions


###### Note


Since version 3.0.0-beta, the `::from::` functions (e.g. `duration::from::millis()`) now use underscores (e.g. `duration::from_millis()`) to better match the intent of the function and method syntax.

These functions can be used when converting between numeric and duration data.

| Function | Description |
| --- | --- |
| duration::days() | Counts how many days fit in a duration |
| duration::hours() | Counts how many hours fit in a duration |
| duration::max | Constant representing the greatest possible duration |
| duration::micros() | Counts how many microseconds fit in a duration |
| duration::millis() | Counts how many milliseconds fit in a duration |
| duration::mins() | Counts how many minutes fit in a duration |
| duration::nanos() | Counts how many nanoseconds fit in a duration |
| duration::secs() | Counts how many seconds fit in a duration |
| duration::weeks() | Counts how many weeks fit in a duration |
| duration::years() | Counts how many years fit in a duration |
| duration::from_days() | Converts a numeric amount of days into a duration that represents days |
| duration::from_hours() | Converts a numeric amount of hours into a duration that represents hours |
| duration::from_micros() | Converts a numeric amount of microseconds into a duration that represents microseconds |
| duration::from_millis() | Converts a numeric amount of milliseconds into a duration that represents milliseconds |
| duration::from_mins() | Converts a numeric amount of minutes into a duration that represents minutes |
| duration::from_nanos() | Converts a numeric amount of nanoseconds into a duration that represents nanoseconds |
| duration::from_secs() | Converts a numeric amount of seconds into a duration that represents seconds |
| duration::from_weeks() | Converts a numeric amount of weeks into a duration that represents weeks |


## duration::days


The `duration::days` function counts how many days fit into a duration.

API DEFINITION

```
duration::days(duration) -> number

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::days(3w);

-- 21

```


## duration::hours


The `duration::hours` function counts how many hours fit into a duration.

API DEFINITION

```
duration::hours(duration) -> number

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::hours(3w);

-- 504

```


## duration::max


The `duration::max` constant represents the greatest possible duration that can be used.

API DEFINITION

```
duration::max -> duration

```

Some examples of the constant in use:

```
duration::max;

duration::max + 1ns;

100y IN 0ns..duration::max

```

Output

```
-------- Query 1 --------

584942417355y3w5d7h15s999ms999µs999ns

-------- Query 2 --------
'Failed to compute: "584942417355y3w5d7h15s999ms999µs999ns + 1ns", as the operation results in an arithmetic overflow.'

-------- Query 3 --------
true

```


## duration::micros


The `duration::micros` function counts how many microseconds fit into a duration.

API DEFINITION

```
duration::micros(duration) -> number

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::micros(3w);

-- 1814400000000

```


## duration::millis


The `duration::millis` function counts how many milliseconds fit into a duration.

API DEFINITION

```
duration::millis(duration) -> number

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::millis(3w);

-- 1814400000

```


## duration::mins


The `duration::mins` function counts how many minutes fit into a duration.

API DEFINITION

```
duration::mins(duration) -> number

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::mins(3w);

-- 30240

```


## duration::nanos


The `duration::nanos` function counts how many nanoseconds fit into a duration.

API DEFINITION

```
duration::nanos(duration) -> number

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::nanos(3w);

-- 1814400000000000

```


## duration::secs


The `duration::secs` function counts how many seconds fit into a duration.

API DEFINITION

```
duration::secs(duration) -> number

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::secs(3w);

-- 1814400

```


## duration::weeks


The `duration::weeks` function counts how many weeks fit into a duration.

API DEFINITION

```
duration::weeks(duration) -> number

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::weeks(3w);

-- 3

```


## duration::years


The `duration::years` function counts how many years fit into a duration.

API DEFINITION

```
duration::years(duration) -> number

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::years(300w);

-- 5

```


## duration::from_days


The `duration::from_days` function counts how many years fit into a duration.

API DEFINITION

```
duration::from_days(number) -> duration

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::from_days(3);

-- 3d

```


## duration::from_hours


The `duration::from_hours` function converts a numeric amount of hours into a duration that represents hours.

API DEFINITION

```
duration::from_hours(number) -> duration

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::from_hours(3);

-- 3h

```


## duration::from_micros


The `duration::from_micros` function converts a numeric amount of microseconds into a duration that represents microseconds.

API DEFINITION

```
duration::from_micros(number) -> duration

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::from_micros(3);

-- 3μs

```


## duration::from_millis


The `duration::from_millis` function converts a numeric amount of milliseconds into a duration that represents milliseconds.

API DEFINITION

```
duration::from_millis(number) -> duration

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::from_millis(3);

-- 3ms

```


## duration::from_mins


The `duration::from_mins` function converts a numeric amount of minutes into a duration that represents minutes.

API DEFINITION

```
duration::from_mins(number) -> duration

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::from_mins(3);

-- 3m

```


## duration::from_nanos


The `duration::from_nanos` function converts a numeric amount of nanoseconds into a duration that represents nanoseconds.

API DEFINITION

```
duration::from_nanos(number) -> duration

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::from_nanos(3);

-- 3ns

```


## duration::from_secs


The `duration::from_secs` function converts a numeric amount of seconds into a duration that represents seconds.

API DEFINITION

```
duration::from_secs(number) -> duration

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::from_secs(3);

-- 3s

```


## duration::from_weeks


The `duration::from_weeks` function converts a numeric amount of weeks into a duration that represents weeks.

API DEFINITION

```
duration::from_weeks(number) -> duration

```

The following example shows this function, and its output, when used in a [RETURN](/docs/surrealql/statements/return) statement:

```
RETURN duration::from_weeks(3);

-- 3w

```


## Method chaining


Method chaining allows functions to be called using the `.` dot operator on a value of a certain type instead of the full path of the function followed by the value.

```
-- Traditional syntax
duration::mins(2d6h);

-- Method chaining syntax
2d6h.mins();

```

Response

```
3240

```

This is particularly useful for readability when a function is called multiple times.

```
-- Traditional syntax
duration::mins(duration::from_millis(98734234));

-- Method chaining syntax
duration::from_millis(98734234).mins();

```

Response

```
1645

```
