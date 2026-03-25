---
title: Crypto functions
url: https://surrealdb.com/docs/surrealql/functions/database/crypto
crawled_at: 2026-03-25 18:43:01
---

# Crypto functions


These functions can be used when hashing data, encrypting data, and for securely authenticating users into the database.

| Function | Description |
| --- | --- |
| crypto::blake3() | Returns the blake3 hash of a value |
| crypto::joaat() | Returns the joaat hash of a value |
| crypto::md5() | Returns the md5 hash of a value |
| crypto::sha1() | Returns the sha1 hash of a value |
| crypto::sha256() | Returns the sha256 hash of a value |
| crypto::sha512() | Returns the sha512 hash of a value |
| crypto::argon2::compare() | Compares an argon2 hash to a password |
| crypto::argon2::generate() | Generates a new argon2 hashed password |
| crypto::bcrypt::compare() | Compares an bcrypt hash to a password |
| crypto::bcrypt::generate() | Generates a new bcrypt hashed password |
| crypto::pbkdf2::compare() | Compares an pbkdf2 hash to a password |
| crypto::pbkdf2::generate() | Generates a new pbkdf2 hashed password |
| crypto::scrypt::compare() | Compares an scrypt hash to a password |
| crypto::scrypt::generate() | Generates a new scrypt hashed password |


## crypto::blake3


The `crypto::blake3` function returns the blake3 hash of the input value.

API DEFINITION

```
crypto::blake3(string) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN crypto::blake3("tobie");-- '85052e9aab1b67b6622d94a08441b09fd5b7aca61ee360416d70de5da67d86ca'
```


## crypto::joaat


The `crypto::joaat` function returns the joaat hash of the input value.

API DEFINITION

```
crypto::joaat(string) -> number
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN crypto::joaat("tobie");-- 2129482046
```


## crypto::md5


The `crypto::md5` function returns the md5 hash of the input value.

API DEFINITION

```
crypto::md5(string) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN crypto::md5("tobie");-- "4768b3fc7ac751e03a614e2349abf3bf"
```


## crypto::sha1


The `crypto::sha1` function returns the sha1 hash of the input value.

API DEFINITION

```
crypto::sha1(string) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN crypto::sha1("tobie");-- "c6be709a1b6429472e0c5745b411f1693c4717be"
```


## crypto::sha256


The `crypto::sha256` function returns the sha256 hash of the input value.

API DEFINITION

```
crypto::sha256(string) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN crypto::sha256("tobie");-- "33fe1859daba927ea5674813adc1cf34b9e2795f2b7e91602fae19c0d0c493af"
```


## crypto::sha512


The `crypto::sha512` function returns the sha512 hash of the input value.

API DEFINITION

```
crypto::sha512(string) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN crypto::sha512("tobie");"39f0160c946c4c53702112d6ef3eea7957ea8e1c78787a482a89f8b0a8860a20ecd543432e4a187d9fdcd1c415cf61008e51a7e8bf2f22ac77e458789c9cdccc"
```


## crypto::argon2::compare


The `crypto::argon2::compare` function compares a hashed-and-salted argon2 password value with an unhashed password value.

API DEFINITION

```
crypto::argon2::compare(string, $against: string) -> bool
```

The following example shows this function, and its output, when used in a RETURN statement:

```
LET $hash = "$argon2id$v=19$m=4096,t=3,p=1$pbZ6yJ2rPJKk4pyEMVwslQ$jHzpsiB+3S/H+kwFXEcr10vmOiDkBkydVCSMfRxV7CA";LET $pass = "this is a strong password";RETURN crypto::argon2::compare($hash, $pass);-- true
```


## crypto::argon2::generate


The `crypto::argon2::generate` function hashes and salts a password using the argon2 hashing algorithm.

###### Important


At this time, there is no way to customize the parameters for this function. This applies to: memory, iterations and parallelism.

API DEFINITION

```
crypto::argon2::generate(string) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN crypto::argon2::generate("this is a strong password");"$argon2id$v=19$m=4096,t=3,p=1$pbZ6yJ2rPJKk4pyEMVwslQ$jHzpsiB+3S/H+kwFXEcr10vmOiDkBkydVCSMfRxV7CA"
```


## crypto::bcrypt::compare


The `crypto::bcrypt::compare` function compares a hashed-and-salted bcrypt password value with an unhashed password value.

API DEFINITION

```
crypto::bcrypt::compare(string, $against: string) -> bool
```

The following example shows this function, and its output, when used in a RETURN statement:

```
LET $hash = "$2b$12$OD7hrr1Hycyk8NUwOekYY.cogCICpUnwNvDZ9NiC1qCPHzpVAQ9BO";LET $pass = "this is a strong password";RETURN crypto::bcrypt::compare($hash, $pass);true
```


## crypto::bcrypt::generate


The `crypto::bcrypt::generate` function hashes and salts a password using the bcrypt hashing algorithm.

###### Important


At this time, there is no way to customize the work factor for bcrypt.

API DEFINITION

```
crypto::bcrypt::generate(string) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN crypto::bcrypt::generate("this is a strong password");"$2b$12$OD7hrr1Hycyk8NUwOekYY.cogCICpUnwNvDZ9NiC1qCPHzpVAQ9BO"
```


## crypto::pbkdf2::compare


The `crypto::pbkdf2::compare` function compares a hashed-and-salted pbkdf2 password value with an unhashed password value.

API DEFINITION

```
crypto::pbkdf2::compare(string, $against: string) -> bool
```

The following example shows this function, and its output, when used in a RETURN statement:

```
LET $hash = "$pbkdf2-sha256$i=10000,l=32$DBURRPJODKEt0IId1Lqe+w$Ve8Z00mibHDSKLbyKTceEBBcDpGoK0AEUl7QzDTIec4";LET $pass = "this is a strong password";RETURN crypto::pbkdf2::compare($hash, $pass);true
```


## crypto::pbkdf2::generate


The `crypto::pbkdf2::generate` function hashes and salts a password using the pbkdf2 hashing algorithm.

###### Important


At this time, there is no way to customize the number of iterations for pbkdf2.

API DEFINITION

```
crypto::pbkdf2::generate(string) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN crypto::pbkdf2::generate("this is a strong password");"$pbkdf2-sha256$i=10000,l=32$DBURRPJODKEt0IId1Lqe+w$Ve8Z00mibHDSKLbyKTceEB"
```


## crypto::scrypt::compare


The `crypto::scrypt::compare` function compares a hashed-and-salted scrypt password value with an unhashed password value.

API DEFINITION

```
crypto::scrypt::compare(string, $against: string) -> bool
```

The following example shows this function, and its output, when used in a RETURN statement:

```
LET $hash = "$scrypt$ln=15,r=8,p=1$8gl7bipl0FELTy46YJOBrw$eRcS1qR22GI8VHo58WOXn9JyfDivGo5yTJFvpDyivuw";LET $pass = "this is a strong password";RETURN crypto::scrypt::compare($hash, $pass);true
```


## crypto::scrypt::generate


The `crypto::scrypt::generate` function hashes and salts a password using the scrypt hashing algorithm.

###### Important


At this time, there is no way to customize the parameters for this function. This applies to: cost parameter, block size and parallelism.

API DEFINITION

```
crypto::scrypt::generate(string) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN crypto::scrypt::generate("this is a strong password");"$scrypt$ln=15,r=8,p=1$8gl7bipl0FELTy46YJOBrw$eRcS1qR22GI8VHo58WOXn9JyfDivGo5yTJFvpDyivuw"
```
