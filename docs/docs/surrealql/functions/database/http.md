---
title: HTTP functions
url: https://surrealdb.com/docs/surrealql/functions/database/http
crawled_at: 2026-03-25 18:43:11
---

# HTTP functions


These functions can be used when opening and submitting remote web requests, and webhooks.

| Function | Description |
| --- | --- |
| http::head() | Perform a remote HTTP HEAD request |
| http::get() | Perform a remote HTTP GET request |
| http::put() | Perform a remote HTTP PUT request |
| http::post() | Perform a remote HTTP POST request |
| http::patch() | Perform a remote HTTP PATCH request |
| http::delete() | Perform a remote HTTP DELETE request |


## Before you begin


From version `2.2` of SurrealDB, the HTTP functions have been improved to provide a more consistent and user-friendly experience. These improvements include:

- Enhanced HTTP error messages: The server provides more descriptive error responses, including relevant HTTP status codes and detailed error information when available.
- Raw SurrealQL data encoding: Data types are preserved more faithfully in responses through improved encoding.SurrealQL byte values are now sent as raw bytes (not base64-encoded or JSON-encoded).SurrealQL string values are sent as raw strings.All other SurrealQL values (numbers, arrays, objects, booleans, etc.) are automatically JSON-encoded.
- Manual Header Configuration: SurrealDB no longer automatically adds Content-Type: application/octet-stream to responses when the body contains SurrealQL byte values. If you need this header, you can set it manually.

## http::head


The `http::head` function performs a remote HTTP `HEAD` request. The first parameter is the URL of the remote endpoint. If the response does not return a `2XX` status code, then the function will fail and return the error.

API DEFINITION

```
http::head(string) -> null
```

If an object is given as the second argument, then this can be used to set the request headers.

API DEFINITION

```
http::head(string, $headers: object) -> null
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN http::head('https://surrealdb.com');null
```

To specify custom headers with the HTTP request, pass an object as the second argument:

```
RETURN http::head('https://surrealdb.com', {	'x-my-header': 'some unique string'});null
```


## http::get


The `http::get` function performs a remote HTTP `GET` request. The first parameter is the URL of the remote endpoint. If the response does not return a 2XX status code, then the function will fail and return the error.

If the remote endpoint returns an `application/json content-type`, then the response is parsed and returned as a value, otherwise the response is treated as text.

API DEFINITION

```
http::get(string) -> value
```

If an object is given as the second argument, then this can be used to set the request headers.

API DEFINITION

```
http::get(string, $headers: object) -> value
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN http::get('https://surrealdb.com');-- The HTML code is returned
```

To specify custom headers with the HTTP request, pass an object as the second argument:

```
RETURN http::get('https://surrealdb.com', {	'x-my-header': 'some unique string'});-- The HTML code is returned
```


## http::put


The `http::put` function performs a remote HTTP `PUT` request. The first parameter is the URL of the remote endpoint, and the second parameter is the value to use as the request body, which will be converted to JSON. If the response does not return a `2XX` status code, then the function will fail and return the error. If the remote endpoint returns an `application/json` content-type, then the response is parsed and returned as a value, otherwise the response is treated as text.

API DEFINITION

```
http::put(string, $body: object) -> value
```

If an object is given as the third argument, then this can be used to set the request headers.

API DEFINITION

```
http::put(string, $body: object, $headers: object) -> value
```

The following example shows this function, and its output, when used in a RETURN statement:

Request without headers

```
RETURN http::put('https://jsonplaceholder.typicode.com/posts/1', {  id: 1,  body: "This is some awesome thinking!",  postId: 100,  user: {    id: 63,    username: 'eburras1q'  }});
```

Request with headers

```
RETURN http::put('https://jsonplaceholder.typicode.com/posts/1', {  id: 1,  body: "This is some awesome thinking!",  postId: 100,  user: {    id: 63,    username: 'eburras1q'  }}, {  'Authorization': 'Bearer your-token-here',  'Content-Type': 'application/json',  'x-custom-header': 'custom-value'});
```

Response

```
{	body: 'This is some awesome thinking!',	id: 1,	postId: 100,	user: {		id: 63,		username: 'eburras1q'	}}
```


## http::post


The `http::post` function performs a remote HTTP `POST` request. The first parameter is the URL of the remote endpoint, and the second parameter is the value to use as the request body, which will be converted to JSON. If the response does not return a `2XX` status code, then the function will fail and return the error. If the remote endpoint returns an `application/json` content-type, then the response is parsed and returned as a value, otherwise the response is treated as text.

API DEFINITION

```
http::post(string, $body: object) -> value
```

If an object is given as the third argument, then this can be used to set the request headers.

API DEFINITION

```
http::post(string, $body: object, $headers: object) -> value
```

The following example shows this function, and its output, when used in a RETURN statement:

Request without headers

```
RETURN http::post('https://jsonplaceholder.typicode.com/posts/', {  id: 1,  body: "This is some awesome thinking!",  postId: 100,  user: {    id: 63,    username: "eburras1q"  }});
```

Request with headers

```
RETURN http::post('https://jsonplaceholder.typicode.com/posts/', {  id: 1,  body: "This is some awesome thinking!",  postId: 100,  user: {    id: 63,    username: "eburras1q"  }}, {  'Authorization': 'Bearer your-token-here',  'Content-Type': 'application/json',  'x-custom-header': 'custom-value'});
```

Response

```
{	body: 'This is some awesome thinking!',	id: 101,	postId: 100,	user: {		id: 63,		username: 'eburras1q'	}}
```


## http::patch


The `http::patch` function performs a remote HTTP `PATCH` request. The first parameter is the URL of the remote endpoint, and the second parameter is the value to use as the request body, which will be converted to JSON. If the response does not return a `2XX` status code, then the function will fail and return the error. If the remote endpoint returns an `application/json` content-type, then the response is parsed and returned as a value, otherwise the response is treated as text.

API DEFINITION

```
http::patch(string, $body: object) -> value
```

If an object is given as the third argument, then this can be used to set the request headers.

API DEFINITION

```
http::patch(string, $body: object, $headers: object) -> value
```

The following example shows this function, and its output, when used in a RETURN statement:

Request without headers

```
RETURN http::patch('https://jsonplaceholder.typicode.com/posts/1', {  id: 1,  body: "This is some awesome thinking!",  postId: 100,  user: {    id: 63,    username: "eburras1q"  }});
```

Setting the request headers

```
RETURN http::patch('https://jsonplaceholder.typicode.com/posts/1', {  id: 1,  body: "This is some awesome thinking!",  postId: 100,  user: {    id: 63,    username: "eburras1q"  }}, {  'Authorization': 'Bearer your-token-here',  'Content-Type': 'application/json',  'x-custom-header': 'custom-value'});
```

RESPONSE

```
{	body: 'This is some awesome thinking!',	id: 1,	postId: 100,	title: 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',	user: {		id: 63,		username: 'eburras1q'	},	userId: 1}
```


## http::delete


The `http::delete` function performs a remote HTTP `DELETE` request. The first parameter is the URL of the remote endpoint, and the second parameter is the value to use as the request body, which will be converted to JSON. If the response does not return a `2XX` status code, then the function will fail and return the error. If the remote endpoint returns an `application/json` content-type, then the response is parsed and returned as a value, otherwise the response is treated as text.

API DEFINITION

```
http::delete(string) -> value
```

If an object is given as the second argument, then this can be used to set the request headers.

API DEFINITION

```
http::delete(string, $headers: object) -> value
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN http::delete('https://jsonplaceholder.typicode.com/posts/1');{}
```

To specify custom headers with the HTTP request, pass an object as the second argument:

```
RETURN http::delete('https://jsonplaceholder.typicode.com/posts/1', {	'x-my-header': 'some unique string'});{}
```
