---
title: Formatters
url: https://surrealdb.com/docs/surrealql/datamodel/formatters
crawled_at: 2026-03-25 21:40:24
---

# Formatters


The [string::is_datetime](/docs/surrealql/functions/database/string#stringisdatetime) and [time::format](/docs/surrealql/functions/database/time#timeformat) functions in SurrealQL accept certain text formats for date/time formatting. The possible formats are listed below.

### Date formatters


| Specifier | Example | Description |
| --- | --- | --- |
| %Y | 2001 | The full proleptic Gregorian year, zero-padded to 4 digits. |
| %C | 20 | The proleptic Gregorian year divided by 100, zero-padded to 2 digits. |
| %y | 01 | The proleptic Gregorian year modulo 100, zero-padded to 2 digits. |
| %m | 07 | Month number (01 to 12), zero-padded to 2 digits. |
| %b | Jul | Abbreviated month name. Always 3 letters. |
| %B | July | Full month name. |
| %h | Jul | Same as %b. |
| %d | 08 | Day number (01 to 31), zero-padded to 2 digits. |
| %e | 8 | Same as %d but space-padded. Same as %_d. |
| %a | Sun | Abbreviated weekday name. Always 3 letters. |
| %A | Sunday | Full weekday name. |
| %w | 0 | Day of the week. Sunday = 0, Monday = 1, ..., Saturday = 6. |
| %u | 7 | Day of the week. Monday = 1, Tuesday = 2, ..., Sunday = 7. (RFC 3339) |
| %U | 28 | Week number starting with Sunday (00 to 53), zero-padded to 2 digits. |
| %W | 27 | Same as %U, but week 1 starts with the first Monday in that year instead. |
| %G | 2001 | Same as %Y but uses the year number in RFC 3339 week date. |
| %g | 01 | Same as %y but uses the year number in RFC 3339 week date. |
| %V | 27 | Same as %U but uses the week number in RFC 3339 week date (01 to 53). |
| %j | 189 | Day of the year (001 to 366), zero-padded to 3 digits. |
| %D | 07/08/01 | Month-day-year format. Same as %m/%d/%y. |
| %x | 07/08/01 | Locale's date representation. |
| %F | 2001-07-08 | Year-month-day format (RFC 3339). Same as %Y-%m-%d. |
| %v | 8-Jul-2001 | Day-month-year format. Same as %e-%b-%Y. |


### Time formatters


| Specifier | Example | Description |
| --- | --- | --- |
| %H | 00 | Hour number (00 to 23), zero-padded to 2 digits. |
| %k | 0 | Same as %H but space-padded. Same as %_H. |
| %I | 12 | Hour number in 12-hour clocks (01 to 12), zero-padded to 2 digits. |
| %l | 12 | Same as %I but space-padded. Same as %_I. |
| %P | am | am or pm in 12-hour clocks. |
| %p | AM | AM or PM in 12-hour clocks. |
| %M | 34 | Minute number (00 to 59), zero-padded to 2 digits. |
| %S | 60 | Second number (00 to 60), zero-padded to 2 digits. |
| %f | 026490000 | The fractional seconds (in nanoseconds) since last whole second. |
| %.f | .026490 | Similar to %f but left-aligned. |
| %.3f | .026 | Similar to .%f but left-aligned but fixed to a length of 3. |
| %.6f | .026490 | Similar to .%f but left-aligned but fixed to a length of 6. |
| %.9f | .026490000 | Similar to .%f but left-aligned but fixed to a length of 9. |
| %3f | 026 | Similar to %.3f but without the leading dot. |
| %6f | 026490 | Similar to %.6f but without the leading dot. |
| %9f | 026490000 | Similar to %.9f but without the leading dot. |
| %R | 00:34 | Hour-minute format. Same as %H:%M. |
| %T | 00:34:59 | Hour-minute-second format. Same as %H:%M:%S. |
| %X | 00:34:59 | Locale's time representation. |
| %r | 12:34:59 AM | Hour-minute-second format in 12-hour clocks. Same as %I:%M:%S %p. |
| %x | 07/08/01 | Locale's date representation. |
| %F | 2001-07-08 | Year-month-day format (RFC 3339). Same as %Y-%m-%d. |
| %v | 8-Jul-2001 | Day-month-year format. Same as %e-%b-%Y. |


### Timezones formatters


| Specifier | Example | Description |
| --- | --- | --- |
| %Z | ACST | Local time zone name. |
| %z | +0930 | Offset from the local time to UTC (with UTC being +0000). |
| %:z | +09:30 | Same as %z but with a colon. |


### Date & time formatters


| Specifier | Example | Description |
| --- | --- | --- |
| %c | Sun Jul 8 00:34:59 2001 | Locale's date and time. |
| %+ | 2001-07-08T00:34:59.026490+09:30 | RFC 3339 / RFC 3339 date & time format. |
| %s | 994518299 | UNIX timestamp, the number of seconds since 1970-01-01T00:00:00. |


### Other formatters


| Specifier | Example | Description |
| --- | --- | --- |
| %t | - | Literal tab (\t). |
| %n | - | Literal newline (\n). |
| %% | - | Literal percent sign. |


## Examples


Seeing if an input with a date and time conforms to an expected format:

```
string::is_datetime("5sep2024pm012345.6789", "%d%b%Y%p%I%M%S%.f");

```

Response

```
true

```

Another example with a different format:

```
string::is_datetime("23:56:00 2015-09-05", "%Y-%m-%d %H:%M");

```

Response

```
false

```

Using a formatter to generate a string from a datetime:

```
time::format(d"2021-11-01T08:30:17+00:00", "%Y-%m-%d");

```

Response

```
"2021-11-01"

```
