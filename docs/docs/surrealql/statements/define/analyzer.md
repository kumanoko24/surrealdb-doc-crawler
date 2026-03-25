---
title: DEFINE ANALYZER statement
url: https://surrealdb.com/docs/surrealql/statements/define/analyzer
crawled_at: 2026-03-25 18:42:27
---

# DEFINE ANALYZER statement


###### Note


Before SurrealDB version 3.0.0-beta, the `FULLTEXT ANALYZER` clause used the syntax `SEARCH ANALYZER`.

In the context of a database, an analyzer plays a crucial role in text processing and searching. It is defined by its name, a set of tokenizers, and a collection of filters.

The output of an analyzer can be experimented with by using the search::analyze() function.

## Requirements


- You must be authenticated as a root, namespace, or database user before you can use the DEFINE ANALYZER statement.
- You must select your namespace and database before you can use the DEFINE ANALYZER statement.

## Statement syntax

SurrealQL SyntaxRailroad Diagram
SurrealQL Syntax

```
DEFINE ANALYZER [ OVERWRITE | IF NOT EXISTS ] @name [ FUNCTION @function ] [ TOKENIZERS @tokenizers ] [ FILTERS @filters ] [ COMMENT @string ]
```
DEFINEANALYZEROVERWRITEIFNOTEXISTS@nameFUNCTION@functionTOKENIZERS@tokenizersFILTERS@filtersCOMMENT@string
## The FUNCTION clause


Using the `FUNCTION` clause allows a user-defined function to be executed on the initial input. The function must take and return a `string`.

```
DEFINE FUNCTION fn::backwardsify($input: string) -> string {    $input.split('').fold('', |$a, $b| $b + $a);};DEFINE ANALYZER backwards FUNCTION fn::backwardsify TOKENIZERS blank;search::analyze("backwards", "I like SurrealDB");
```

Output

```
[	'BDlaerruS',	'ekil',	'I']
```

## Tokenizers


Tokenizers are responsible for breaking down a given text into individual tokens based on a set of instructions. There are a couple of tokenizers that can be used while defining an analyzer as seen below:

### blank


The blank tokenizer breaks down a text into tokens by creating a new token each time it encounters a space, tab, or newline character. It's a straightforward way to split text into words or chunks based on whitespace.

```
DEFINE ANALYZER example_blank TOKENIZERS blank;search::analyze("example_blank", "hello world");
```

Output

```
[	'hello',	'world']
```

### camel


The camel tokenizer is used for identifying and creating tokens when the next character in the text is uppercase. This is particularly useful for processing camelCase or PascalCase text, common in programming, to split them into meaningful words.

```
DEFINE ANALYZER example_camel TOKENIZERS camel;search::analyze("example_camel", "helloWorld");
```

Output

```
[	'hello',	'World']
```

### class


The class tokenizer segments text into tokens by detecting changes (digit, letter, punctuation, blank) in the Unicode class of characters. It creates a new token when the character class changes, distinguishing between digits, letters, punctuation, and blanks. This allows for flexible tokenization based on character types.

```
DEFINE ANALYZER example_class TOKENIZERS class;search::analyze("example_class", "123abc!XYZ");
```

Output

```
[	'123',	'abc',	'!',	'XYZ']
```

### punct


The punct tokenizer generates tokens by breaking the text whenever a punctuation character is encountered. It's suitable for tokenizing sentences or breaking text into smaller units based on punctuation marks.

```
DEFINE ANALYZER example_punct TOKENIZERS punct;search::analyze("example_punct", "Hello, World!");
```

Output

```
[	'Hello',	',',	'World',	'!']
```

## Filters


Filters take on the task of transforming these tokens for further processing and analysis.

### ascii


The ascii filter is responsible for processing tokens by replacing or removing diacritical marks (accents and special characters) from the text. It helps standardize text by converting accented characters to their basic ASCII equivalents, making it more suitable for various text analysis tasks.

```
DEFINE ANALYZER example_ascii TOKENIZERS class FILTERS ascii;search::analyze("example_ascii", "résumé café");
```

Output

```
[	'resume',	'cafe']
```

### lowercase


The lowercase filter converts tokens to lowercase, ensuring that text is consistently in lowercase format. This is often used to make text case-insensitive for search and analysis purposes.

```
DEFINE ANALYZER example_lowercase TOKENIZERS class FILTERS lowercase;search::analyze("example_lowercase", "Hello World");
```

Output

```
[	'hello',	'world']
```

### uppercase


The uppercase filter converts tokens to uppercase, ensuring text consistency in uppercase format. It can be useful when case-insensitivity is required for specific analysis or search operations.

For example, if you had the text **"Hello World"**, the uppercase filter would create two tokens, **["HELLO", "WORLD"]**. Below is an example of how to use the uppercase filter:

```
DEFINE ANALYZER example_uppercase TOKENIZERS class FILTERS uppercase;search::analyze("example_uppercase", "Hello World");
```

Output

```
[	'HELLO',	'WORLD']
```

### edgengram(min,max)


The edgengram filter is used to create tokens that represent prefixes of terms. It generates a sequence of tokens that gradually build up a term, which can be useful for autocomplete or searching based on partial words. It accepts two parameters `min` and `max` which define the minimum and maximum amount of characters in the prefix.

For example, if you had the text **"apple banana"**, the edgengram filter would create six tokens, **["a", "ap", "app", "b", "ba", "ban"]**. Below is an example of how to use the edgengram filter:

```
DEFINE ANALYZER example_edgengram TOKENIZERS class FILTERS edgengram(1,3);search::analyze("example_edgengram", "apple banana");
```

```
[	'a',	'ap',	'app',	'b',	'ba',	'ban']
```

### mapper(path)


The mapping filter is designed to enable lemmatization within SurrealDB.

Lemmatization is the process of reducing words to their base or dictionary form. The mapper mechanism allows users to specify a custom dictionary file that maps terms to their base forms. This dictionary file is then used by SurrealDB’s analyzer to standardize terms as they are indexed, improving search consistency.

This is particularly useful for handling irregular verbs and other terms that the default "snowball" filter cannot handle. Lemmatization files are easy to put together and to find online, making it possible to customize full-text search for smaller languages.

How does the mapper work?

Configuration: In the SQL statement below, the mapper parameter is specified within the analyzer definition.
This parameter points to the file that contains the term mappings for lemmatization.

```
DEFINE ANALYZER lemme_english TOKENIZERS blank,class FILTERS lowercase,mapper('../tests/data/lemmatization-en.txt');RETURN [    search::analyze("lemme_english", "He drove and swam"),];
```

Output

```
[	[		'he',		'drive',		'and',		'swim'	]]
```

Dictionary File Structure: The file specified in the mapper parameter must follow this format:

- Each line contains a pair of terms separated by a tab.
- The first term represents the canonical (base form) of the word.
- The second term is the form to be mapped to this base form.

Example file format:

```
drive	drivendrive	drivesdrive	drivingdrive	droveswim	swamswim	swimmingswim	swimsswim	swum
```

Usage: When this analyzer is applied to a text, any word that matches the mapped term in the dictionary file will be replaced by its base form before indexing. This helps ensure consistency in search results by consolidating different forms of a word to a single, standardized entry.

By using this custom dictionary-based mapper, you can control how irregular forms and other variations of terms are indexed,
making search behavior more predictable and comprehensive.

The following example shows how lemmatization can be used to generate a list of words and their respective frequencies. Other notable functionalities in the example are the string::is_alpha() function inside array::filter() to remove all non-alphabetic strings, the type::record() function to construct a record ID from two strings, and an UPSERT statement to create a record if one does not exist, or update it otherwise.

```
DEFINE ANALYZER lemme_english TOKENIZERS blank,class FILTERS lowercase,mapper('../tests/data/lemmatization-en.txt');LET $text = "The Wheel of Time turns, and Ages come and pass, leaving memories that become legend. Legend fades to myth, and even myth is long forgotten when the Age that gave it birth comes again. In one Age, called the Third Age by some, an Age yet to come, an Age long past, a wind rose in the Mountains of Mist. The wind was not the beginning. There are neither beginnings nor endings to the turning of the Wheel of Time. But it was a beginning.";LET $words = search::analyze("lemme_english", $text)    .filter(|$c| $c.is_alpha());FOR $word IN $words {    UPSERT type::record("word", $word) SET frequency += 1;};SELECT * FROM word WHERE frequency >=3 ORDER BY frequency DESC;
```

Output

```
[	{		frequency: 8,		id: word:the	},	{		frequency: 6,		id: word:age	},	{		frequency: 4,		id: word:a	},	{		frequency: 4,		id: word:be	},	{		frequency: 4,		id: word:of	},	{		frequency: 3,		id: word:and	},	{		frequency: 3,		id: word:come	},	{		frequency: 3,		id: word:to	}]
```

A mapper can also be used for ad-hoc filtering, as long as the file referenced contains two single words separated by a tab. Take the following file for example:

```
NOT_FOUND	File_not_foundNOT_FOUND	Datei_nicht_gefundenNOT_FOUND	Fichier_non_trouvéTIMEOUT	Timed_outTIMEOUT	Délai_expiréTIMEOUT	Zeitüberschreitung
```

An analyzer that uses a single mapper filter can then use this lemmatizer to unify multilingual error messages into a single output.

```
DEFINE ANALYZER error_filter FILTERS mapper('error_filter.txt');LET $messages = 	["File not found", "Datei nicht gefunden", "Zeitüberschreitung"]	.map(|$word| $word.replace(' ', '_'))	.join(' ');search::analyze("error_filter", $messages);
```

Output

```
[	'NOT_FOUND',	'NOT_FOUND',	'TIMEOUT']
```

Example using the same mapper to search for errors in multiple languages:

```
DEFINE ANALYZER error_filter FILTERS mapper('error_filter.txt');DEFINE INDEX OVERWRITE errors ON TABLE error FIELDS message FULLTEXT ANALYZER error_filter;FOR $message IN ["File not found", "Datei nicht gefunden", "Zeitüberschreitung"] {	CREATE error SET message = $message.replace(' ', '_'), at = time::now();};SELECT * FROM error WHERE message @@ "NOT_FOUND";
```

Output

```
[	{		at: d'2024-11-13T03:56:12.039252Z',		id: error:acbc044syhnx54wzs3n9,		message: 'File_not_found'	},	{		at: d'2024-11-13T03:56:12.043643Z',		id: error:5ifxic9s750x24ts4zof,		message: 'Datei_nicht_gefunden'	}]
```

### ngram(min,max)


The ngram filter is used to create a sequence of 'n' tokens from a given sample of text or speech. These items can be syllables, letters, words or base pairs according to the application. It accepts two parameters `min` and `max` which indicates that you want to create n-grams starting from min to size of max.

```
DEFINE ANALYZER example_ngram TOKENIZERS class FILTERS ngram(1,3);search::analyze("example_ngram", "apple banana");
```

Output

```
[	'a',	'ap',	'app',	'p',	'pp',	'ppl',	'p',	'pl',	'ple',	'l',	'le',	'e',	'b',	'ba',	'ban',	'a',	'an',	'ana',	'n',	'na',	'nan',	'a',	'an',	'ana',	'n',	'na',	'a']
```

### snowball(language)


The snowball filter applies Snowball stemming to tokens, reducing them to their root form and converts the case to lowercase. The following supported languages can be passed as a parameter in snowball: Arabic, Danish, Dutch, English, French, German, Greek, Hungarian, Italian, Norwegian, Portuguese, Romanian, Russian, Spanish, Swedish, Tamil, Turkish.

```
DEFINE ANALYZER english_snowball TOKENIZERS class FILTERS snowball(english);DEFINE ANALYZER german_snowball TOKENIZERS class FILTERS snowball(german);RETURN [    search::analyze("english_snowball", "Looking at some running cats"),    search::analyze("german_snowball", "Sollen wir was trinken gehen?")];
```

Output

```
[	[		'look',		'at',		'some',		'run',		'cat'	],	[		'soll',		'wir',		'was',		'trink',		'geh',		'?'	]]
```

## Using IF NOT EXISTS clause


The `IF NOT EXISTS` clause can be used to define an analyzer only if it does not already exist. You should use the `IF NOT EXISTS` clause when defining an analyzer in SurrealDB if you want to ensure that the analyzer is only created if it does not already exist. If the analyzer already exists, the `DEFINE ANALYZER` statement will return an error.

It's particularly useful when you want to safely attempt to define a analyzer without manually checking its existence first.

On the other hand, you should not use the `IF NOT EXISTS` clause when you want to ensure that the analyzer definition is updated regardless of whether it already exists. In such cases, you might prefer using the `OVERWRITE` clause, which allows you to define a analyzer and overwrite an existing one if it already exists, ensuring that the latest version of the analyzer definition is always in use.

```
-- Create an ANALYZER if it does not already existDEFINE ANALYZER IF NOT EXISTS example TOKENIZERS blank;
```

## Using OVERWRITE clause


The `OVERWRITE` clause can be used to create an analyzer and overwrite an existing one if it already exists. You should use the `OVERWRITE` clause when you want to modify an existing analyzer definition. If the analyzer already exists, the `DEFINE ANALYZER` statement will overwrite the existing analyzer definition with the new one.

```
-- Create an ANALYZER and overwrite if it already existsDEFINE ANALYZER OVERWRITE example TOKENIZERS blank;
```

## More examples


Examples on application of analyzers to indexes can be found in the documenation on DEFINE INDEX statement

This example creates an analyzer that tokenizes text based on the class of characters and then applies the lowercase filter to the tokens.

```
-- Creates a simple analyzer removing diacritics marksDEFINE ANALYZER ascii TOKENIZERS class FILTERS lowercase,ascii;
```

This example creates an analyzer specifically designed for processing English texts.

```
-- Creates an analyzer suitable for English textDEFINE ANALYZER english TOKENIZERS class FILTERS snowball(english);
```

This example creates an analyzer specifically designed for auto-completion tasks.

```
-- Creates an analyzer suitable for auto-completion.DEFINE ANALYZER autocomplete FILTERS lowercase,edgengram(2,10);
```

This example creates an analyzer specifically designed for source code analysis.

```
-- Creates an analyzer suitable for source code analysis.DEFINE ANALYZER code TOKENIZERS class,camel FILTERS lowercase,ascii;
```
