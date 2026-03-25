---
title: Encoding functions
url: https://surrealdb.com/docs/surrealql/functions/database/encoding
crawled_at: 2026-03-25 19:09:58
---

# Encoding functions

These functions can be used to encode and decode data into other formats, such as `base64` and [`CBOR` (Concise Binary Object Representation). It is particularly used when that data needs to be stored and transferred over media that are designed to deal with text. This encoding and decoding helps to ensure that the data remains intact without modification during transport.


| Function |Description | |
| `encoding::base64::decode()` |This function is used to decode data. | |
| `encoding::base64::encode()` | This function is used to encode data with optionally padded output. | |
| `encoding::cbor::decode()` |This function is used to decode data. | |
| `encoding::cbor::encode()` |This function is used to encode data. | |


## `encoding::base64::encode()`

The `encoding::base64::encode()` function encodes a bytes to base64 with optionally padded output.

```encoding::base64::encode(bytes) -> string

```

```encoding::base64::encode(bytes, $pad_output: option<bool>) -> string

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN encoding::base64::encode(<bytes>"");

-- ''

```

```RETURN encoding::base64::encode(<bytes>"2323");

-- 'MjMyMw'

```

```RETURN encoding::base64::encode(<bytes>"hello");

-- 'aGVsbG8'

```

As of version 2.3.0, you can pass `true` as the second argument to enable padded base64 outputs:

```RETURN encoding::base64::encode(<bytes>"", true);

-- ""

```

```RETURN encoding::base64::encode(<bytes>"2323", true);

"MjMyMw=="

```

```RETURN encoding::base64::encode(<bytes>"hello", true);

"aGVsbG8="

```


## `encoding::base64::decode()`

The `encoding::base64::decode()` function decodes a string into bytes.

API DEFINITION

```encoding::base64::decode(string) -> bytes

```

The following example shows this function, and its output, when used in a [`RETURN` statement:

```RETURN encoding::base64::decode("MjMyMw");

-- b"32333233"

```

You can also verify that the output of the encoded value matches the original value. 

```RETURN encoding::base64::decode("aGVsbG8") = <bytes>"hello";

-- true

```


## `encoding::cbor::decode()`

The `encoding::cbor::decode()` function decodes bytes in valid CBOR format into a SurrealQL value.

API DEFINITION

```encoding::cbor::decode(string) -> any

```

```LET $some_bytes = encoding::base64::decode("omRjYm9yaGVuY29kaW5nYmlza3ByZXR0eSBuZWF0");
encoding::cbor::decode($some_bytes);

```

Output

```{
	cbor: 'encoding',
	is: 'pretty neat'
}

```


## `encoding::cbor::encode()`

The `encoding::cbor::encode()` function encodes any SurrealQL value into bytes in CBOR format.

API DEFINITION

```encoding::cbor::encode(any) -> bytes

```

```encoding::cbor::encode({
    cbor: "encoding",
    is: "pretty neat"
});

```

Output

```b"A26463626F7268656E636F64696E676269736B707265747479206E656174"

```
