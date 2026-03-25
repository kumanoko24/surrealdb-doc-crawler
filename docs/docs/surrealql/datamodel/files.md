---
title: Files
url: https://surrealdb.com/docs/surrealql/datamodel/files
crawled_at: 2026-03-25 18:40:28
---

# Files


Files are accessed by a path, which is prefixed with an `f` to differentiate it from a regular string.

Some examples of file pointers:

```
f"bucket:/some/key/to/a/file.txt";f"bucket:/some/key/with\ escaped";
```

To work with the files that can be accessed through these pointers, use the following:

- A DEFINE BUCKET statement to set up the bucket to hold the files
- Files functions such as file::put() and file::get()

```
DEFINE BUCKET my_bucket BACKEND "memory";f"my_bucket:/some_file.txt".put("Some text inside");f"my_bucket:/some_file.txt".get();<string>f"my_bucket:/some_file.txt".get();
```

Output

```
-------- Query --------b"536F6D65207465787420696E73696465"-------- Query --------'Some text inside'
```

## Using files for ad-hoc memory storage


A combination of files and SurrealDB's encoding functions can be used to set up ad-hoc memory storage. This can be convenient when running an instance that saves data to disk but prefers to keep certain items in memory.

The following example shows how this pattern might be used for temporary storage such as a user's shopping cart during a single session.

```
# Set the allowlist env var to allow the directory to be accessesSURREAL_BUCKET_FOLDER_ALLOWLIST="/users/your_user_name" surreal start --allow-experimental files
```

```
-- Set up the in-memory backendDEFINE BUCKET my_bucket BACKEND "file:/users/your_user_name";-- Convenience functions to save, decode back into-- SurrealQL type, and deleteDEFINE FUNCTION fn::save_file($file_name: string, $input: any) {    LET $file = type::file("shopping_carts", $file_name);    $file.put(encoding::cbor::encode($input));};DEFINE FUNCTION fn::get_file($file_name: string) -> object {    encoding::cbor::decode(type::file("shopping_carts", $file_name).get())};DEFINE FUNCTION fn::delete_file($file_name: string) {    type::file("shopping_carts", $file_name).delete();};-- Save current shopping cartfn::save_file("temp_cart_user_24567", {    items: ["shirt1"],    last_updated: time::now()});fn::get_file("temp_cart_user_24567");-- Returns { items: ['shirt1', 'deck_of_cards'], last_updated: d'2025-11-20T01:03:24.141080Z' }-- User adds item, save over file with newer informationfn::save_file("temp_cart_user_24567", {    items: ["shirt1", "deck_of_cards"],    last_updated: time::now()});fn::get_file("temp_cart_user_24567");-- Returns { items: ['shirt1', 'deck_of_cards'], last_updated: d'2025-11-20T01:06:02.752429Z' }-- Session is over, delete temp filefn::delete_file("temp_cart_user_24567");
```
