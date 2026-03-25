---
title: Time Functions
url: https://surrealdb.com/docs/surrealql/functions/database/time
crawled_at: 2026-03-25 19:09:43
---

# Time Functions

###### Note

Since version 3.0.0-beta, the `::from::` functions (e.g. `time::from::millis()`) now use underscores (e.g. `time::from_millis()`) to better match the intent of the function and method syntax.

These functions can be used when working with and manipulating [datetime values.

Many time functions take an `option<datetime>` in order to return certain values from a datetime such as its hours, minutes, day of the year, and so in. If no argument is present, the current datetime will be extracted and used. As such, all of the following function calls are valid and will not return an error.

```time::hour(d'2024-09-04T00:32:44.107Z');
time::hour();

time::minute(d'2024-09-04T00:32:44.107Z');
time::minute();

time::yday(d'2024-09-04T00:32:44.107Z');
time::yday();

```


| Function |Description | |
| `time::ceil()` |Rounds a datetime up to the next largest duration | |
| `time::day()` |Extracts the day as a number from a datetime or current datetime | |
| `time::epoch` |Constant datetime representing the UNIX epoch | |
| `time::floor()` |Rounds a datetime down by a specific duration | |
| `time::format()` |Outputs a datetime according to a specific format | |
| `time::group()` |Groups a datetime by a particular time interval | |
| `time::hour()` |Extracts the hour as a number from a datetime or current datetime | |
| `time::max()` |Returns the greatest datetime from an array | |
| `time::maximum` |Constant representing the greatest possible datetime | |
| `time::micros()` |Extracts the microseconds as a number from a datetime or current datetime | |
| `time::millis()` |Extracts the milliseconds as a number from a datetime or current datetime | |
| `time::min()` |Returns the least datetime from an array | |
| `time::minimum` |Constant representing the least possible datetime | |
| `time::minute()` |Extracts the minutes as a number from a datetime or current datetime | |
| `time::month()` |Extracts the month as a number from a datetime or current datetime | |
| `time::nano()` |Returns the number of nanoseconds since the UNIX epoch until a datetime or current datetime | |
| `time::now()` |Returns the current datetime | |
| `time::round()` |Rounds a datetime to the nearest multiple of a specific duration | |
| `time::second()` |Extracts the second as a number from a datetime or current datetime | |
| `time::timezone()` |Returns the current local timezone offset in hours | |
| `time::unix()` |Returns the number of seconds since the UNIX epoch | |
| `time::wday()` |Extracts the week day as a number from a datetime or current datetime | |
| `time::week()` |Extracts the week as a number from a datetime or current datetime | |
| `time::yday()` |Extracts the yday as a number from a datetime or current datetime | |
| `time::year()` |Extracts the year as a number from a datetime or current datetime | |
| `time::is_leap_year()` |Checks if given datetime is a leap year | |
| `time::from_micros()` |Calculates a datetime based on the microseconds since January 1, 1970 0:00:00 UTC. | |
| `time::from_millis()` |Calculates a datetime based on the milliseconds since January 1, 1970 0:00:00 UTC. | |
| `time::from_nanos()` |Calculates a datetime based on the nanoseconds since January 1, 1970 0:00:00 UTC. | |
| `time::from_secs()` |Calculates a datetime based on the seconds since January 1, 1970 0:00:00 UTC. | |
| `time::from_unix()` |Calculates a datetime based on the seconds since January 1, 1970 0:00:00 UTC. | |
| `time::from_ulid()` |Calculates a datetime based on the ULID. | |
| `time::from_uuid()` |Calculates a datetime based on the UUID. | |
| `time::set_year()` |Sets the year value of a datetime. | |
| `time::set_month()` |Sets the year value of a datetime. | |
| `time::set_day()` |Sets the year value of a datetime. | |
| `time::set_hour()` |Sets the year value of a datetime. | |
| `time::set_minute()` |Sets the year value of a datetime. | |
| `time::set_second()` |Sets the year value of a datetime. | |
| `time::set_nanosecond()` |Sets the year value of a datetime. | |
## `time::ceil`

The `time::ceil` function rounds a datetime up to the next largest duration.

API DEFINITION

```time::ceil(datetime, $ceiling: duration) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```LET $now = d'2024-08-30T02:22:50.231631Z';

RETURN [
  time::ceil($now, 1h),
  time::ceil($now, 1w)
];

```

Output

```[
	d'2024-08-30T03:00:00Z',
	d'2024-09-05T00:00:00Z'
]

```

## `time::day`

The `time::day` function extracts the day as a number from a datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::day(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::day(d"2021-11-01T08:30:17+00:00");

-- 1

```


## `time::epoch`

The `time::epoch` constant returns the `datetime` for the UNIX epoch (January 1, 1970).

```// Return the const
RETURN time::epoch;
-- d'1970-01-01T00:00:00Z'

// Define field using the const
DEFINE FIELD since_epoch ON event COMPUTED time::now().floor(1d) - time::epoch;
CREATE ONLY event:one SET information = "Something happened";
-- { id: event:one, information: 'Something happened', since_epoch: 55y42w6d }

```


## `time::floor`

The `time::floor` function rounds a datetime down by a specific duration.

API DEFINITION

```time::floor(datetime, $floor: duration) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::floor(d"2021-11-01T08:30:17+00:00", 1w);

-- d'2021-10-28T00:00:00Z'

```


## `time::format`

The `time::format` function outputs a datetime as a string according to a specific format.

API DEFINITION

```time::format(datetime, $format: string) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::format(d"2021-11-01T08:30:17+00:00", "%Y-%m-%d");

```

```'2021-11-01'

```

[View all format options


## `time::group`

The `time::group` function reduces and rounds a datetime down to a particular time interval.

API DEFINITION

```time::group(datetime, $group_by: 'year'|'month'|'day'|'hour'|'minute'|'second') -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::group(d"2021-11-01T08:30:17+00:00", "year");

d'2021-01-01T00:00:00Z'

```


## `time::hour`

The `time::hour` function extracts the hour as a number from a datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::hour(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::hour(d"2021-11-01T08:30:17+00:00");

-- 8

```


## `time::max`

The `time::max` function returns the greatest datetime from an array of datetimes.

API DEFINITION

```time::max(array<datetime>) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::max([ d"1987-06-22T08:30:45Z", d"1988-06-22T08:30:45Z" ])

-- d'1988-06-22T08:30:45Z'

```

See also:

- 
[`array::max`, which extracts the greatest value from an array of values

- 
[`math::max`, which extracts the greatest number from an array of numbers


## `time::maximum`

The `time::maximum` constant returns the greatest possible datetime that can be used.

API DEFINITION

```time::maximum -> datetime

```

Some examples of the constant in use:

```time::maximum;

time::maximum + 1ns;

time::now() IN time::minimum..time::maximum;

```

Output

```-------- Query 1 --------

d'+262142-12-31T23:59:59.999Z'

-------- Query 2 --------

"Failed to compute: \"1ns + d'+262142-12-31T23:59:59.999999999Z'\", as the operation results in an arithmetic overflow."

-------- Query 3 --------

true

```


## `time::micros`

The `time::micros` function extracts the microseconds as a number from a datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::micros(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::micros(d"1987-06-22T08:30:45Z");

-- 551349045000000

```


## `time::millis`

The `time::millis` function extracts the milliseconds as a number from a datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::millis(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::millis(d"1987-06-22T08:30:45Z");

-- 551349045000

```


## `time::min`

The `time::min` function returns the least datetime from an array of datetimes.

API DEFINITION

```time::min(array<datetime>) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::min([ d"1987-06-22T08:30:45Z", d"1988-06-22T08:30:45Z" ]);

-- d'1987-06-22T08:30:45Z'

```

See also:

- 
[`array::min`, which extracts the least value from an array of values

- 
[`math::min`, which extracts the least number from an array of numbers


## `time::minimum`

The `time::minimum` constant returns the least possible datetime that can be used.

API DEFINITION

```time::minimum -> datetime

```

Some examples of the constant in use:

```time::minimum;

time::now() IN time::minimum..time::maximum;

```

Output

```-------- Query 1 --------

d'-262143-01-01T00:00:00Z'

-------- Query 2 --------

true

```


## `time::minute`

The `time::minute` function extracts the minutes as a number from a datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::minute(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::minute(d"2021-11-01T08:30:17+00:00");

-- 30

```


## `time::month`

The `time::month` function extracts the month as a number from a datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::month(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::month(d"2021-11-01T08:30:17+00:00");

-- 11

```


## `time::nano`

The `time::nano`function returns a datetime as an integer representing the number of nanoseconds since the UNIX epoch until a datetime, or the current date if no datetime argument is present.

API DEFINITION

```time::nano(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::nano(d"2021-11-01T08:30:17+00:00");

-- 1635755417000000000

```


## `time::now`

The `time::now` function returns the current datetime as an ISO8601 timestamp.

API DEFINITION

```time::now() -> datetime

```


## `time::round`

The `time::round` function rounds a datetime up by a specific duration.

API DEFINITION

```time::round(datetime, $round_to: duration) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::round(d"2021-11-01T08:30:17+00:00", 1w);

-- d'2021-11-04T00:00:00Z'

```


## `time::second`

The `time::second` function extracts the second as a number from a datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::second(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::second(d"2021-11-01T08:30:17+00:00");

-- 17

```


## `time::timezone`

The `time::timezone` function returns the current local timezone offset in hours.

API DEFINITION

```time::timezone() -> string

```


## `time::unix`

The `time::unix` function returns a datetime as an integer representing the number of seconds since the UNIX epoch until a certain datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::unix(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::unix(d"2021-11-01T08:30:17+00:00");

-- 1635755417

```


## `time::wday`

The `time::wday` function extracts the week day as a number from a datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::wday(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::wday(d"2021-11-01T08:30:17+00:00");

-- 1

```


## `time::week`

The `time::week` function extracts the week as a number from a datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::week(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::week(d"2021-11-01T08:30:17+00:00");

-- 44

```


## `time::yday`

The `time::yday` function extracts the day of the year as a number from a datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::yday(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::yday(d"2021-11-01T08:30:17+00:00");

-- 305

```


## `time::year`

The `time::year` function extracts the year as a number from a datetime, or from the current date if no datetime argument is present.

API DEFINITION

```time::year(option<datetime>) -> number

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::year(d"2021-11-01T08:30:17+00:00");

-- 2021

```


## `time::is_leap_year()`

The `time::is_leap_year()` function Checks if given datetime is a leap year.

API DEFINITION

```time::is_leap_year(datetime) -> bool

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```-- Checks with current datetime if none is passed
RETURN time::is_leap_year();

RETURN time::is_leap_year(d"1987-06-22T08:30:45Z");
-- false

RETURN time::is_leap_year(d"1988-06-22T08:30:45Z");
-- true

-- Using function via method chaining
RETURN d'2024-09-03T02:33:15.349397Z'.is_leap_year();
-- true

```

## `time::from_micros`

The `time::from_micros` function calculates a datetime based on the microseconds since January 1, 1970 0:00:00 UTC.

API DEFINITION

```time::from_micros(number) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::from_micros(1000000);

-- d'1970-01-01T00:00:01Z'

```


## `time::from_millis`

The `time::from_millis` function calculates a datetime based on the milliseconds since January 1, 1970 0:00:00 UTC.

API DEFINITION

```time::from_millis(number) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::from_millis(1000);

-- d'1970-01-01T00:00:01Z'

```


## `time::from_nanos`

The `time::from_nanos` function calculates a datetime based on the nanoseconds since January 1, 1970 0:00:00 UTC.

API DEFINITION

```time::from_nanos(number) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::from_nanos(1000000);

-- d'1970-01-01T00:00:00.001Z'

```


## `time::from_secs`

The `time::from_secs` function calculates a datetime based on the seconds since January 1, 1970 0:00:00 UTC.

API DEFINITION

```time::from_secs(number) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::from_secs(1000);

-- d'1970-01-01T00:16:40Z'

```


## `time::from_unix`

The `time::from_unix` function calculates a datetime based on the seconds since January 1, 1970 0:00:00 UTC.

API DEFINITION

```time::from_unix(number) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::from_unix(1000);

-- d'1970-01-01T00:16:40Z'

```


## `time::from_ulid`

The `time::from_ulid` function calculates a datetime based on the ULID.

API DEFINITION

```time::from_ulid(ulid) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::from_ulid("01JH5BBTK9FKTGSDXHWP5YP9TQ");

-- d'2025-01-09T10:57:03.593Z'

```

As a ULID is only precise up to the millisecond, a conversion from a ULID to a timestamp will truncate nanosecond precision.

```LET $now = time::now();
[$now, time::from_ulid(rand::ulid($now))];

-- Output:
[
	d'2026-01-29T02:07:06.494218Z',
	d'2026-01-29T02:07:06.494Z'
]

```


## `time::from_uuid`

The `time::from_uuid` function calculates a datetime based on the UUID.

API DEFINITION

```time::from_uuid(uuid) -> datetime

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN time::from_uuid(u'01944ab6-c1e5-7760-ab6a-127d37eb1b94');

-- d'2025-01-09T10:57:58.757Z'

```

As a UUID is only precise up to the millisecond, a conversion from a UUID to a timestamp will truncate nanosecond precision.

```LET $now = time::now();
[$now, time::from_uuid(rand::uuid($now))];

-- Output:
[
	d'2026-01-29T02:12:13.848476Z',
	d'2026-01-29T02:12:13.848Z'
]

```


## `time::set_year`

The `time::set_year` function sets the year value of a datetime.

API DEFINITION

```time::set_year(datetime, $year: integer) -> datetime

```

Example:

```d'1970-01-01T00:00:00.500000005Z'.set_year(2026);
-- Output
d'2026-01-01T00:00:00.500000000Z'

```

## `time::set_month`

The `time::set_month` function sets the month value of a datetime.

API DEFINITION

```time::set_month(datetime, $month: integer) -> datetime

```

Example:

```d'1970-01-01T00:00:00.500000005Z'.set_month(9);
-- Output
d'1970-09-01T00:00:00.500000005Z'

```

## `time::set_day`

The `time::set_day` function sets the day value of a datetime.

API DEFINITION

```time::set_day(datetime, $day: integer) -> datetime

```

Example:

```d'1970-01-01T00:00:00.500000005Z'.set_day(10);
-- Output
d'1970-01-10T00:00:00.500000005Z'

```

## `time::set_hour`

The `time::set_hour` function sets the hour value of a datetime.

API DEFINITION

```time::set_hour(datetime, $hour: integer) -> datetime

```

Example:

```d'1970-01-01T00:00:00.500000005Z'.set_hour(10);
-- Output
d'1970-01-01T10:00:00.500000005Z'

```

## `time::set_minute`

The `time::set_minute` function sets the minute value of a datetime.

API DEFINITION

```time::set_minute(datetime, $minute: integer) -> datetime

```

Example:

```d'1970-01-01T10:00:00.500000005Z'.set_minute(55);
-- Output
d'1970-01-01T10:55:00.500000005Z'

```

## `time::set_second`

The `time::set_second` function sets the second value of a datetime.

API DEFINITION

```time::set_second(datetime, $second: integer) -> datetime

```

Example:

```d'1970-01-01T10:00:00.500000005Z'.set_second(30);
-- Output
d'1970-01-01T10:00:30.500000005Z'

```

## `time::set_nanosecond`

The `time::set_nanosecond` function sets the nanosecond value of a datetime.

API DEFINITION

```time::set_nanosecond(datetime, $nanosecond: integer) -> datetime

```

Example:

```d'1970-01-01T10:00:00.500000005Z'.set_nanosecond(3535);
-- Output
d'1970-01-01T10:00:00.000003535Z'

```

Since nanoseconds are not needed in a datetime, setting the nanoseconds of a datetime to 0 can be used to make a datetime look cleaner.

```d'1970-01-01T00:00:00.500000000Z'.set_nanosecond(0);
d'1970-01-01T00:00:00Z' -- output

```
