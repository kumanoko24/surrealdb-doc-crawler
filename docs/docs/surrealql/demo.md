---
title: Demo data
url: https://surrealdb.com/docs/surrealql/demo
crawled_at: 2026-03-25 18:40:15
---

# Demo data


To quickly test out SurrealDB and SurrealQL functionality, we've included two demo datasets here in `.surql` files which you can download and import into SurrealDB using the CLI.

## Surreal Deal Store - there is a lot in store for you!


Surreal Deal Store is our new and improved demo dataset based on our SurrealDB Store.
The dataset is made up of 12 tables using both graph relations and record links.

In the diagram below, the nodes in pink are the standard tables, the ones in purple represent the edge tables which shows relationships between records and SurrealDB as a graph database. The nodes in grey are the pre-computed table views.

### Download

SurrealDB 2.xSurrealDB 3.x
| Dataset | URL |
| --- | --- |
| Surreal Deal Store | https://datasets.surrealdb.com/surreal-deal-store.surql |
| Surreal Deal Store (mini) | https://datasets.surrealdb.com/surreal-deal-store-mini.surql |


| Dataset | URL |
| --- | --- |
| Surreal Deal Store (mini) | https://datasets.surrealdb.com/datasets/surreal-deal-store/mini-v3.surql |


### Import


Once one of the datasets has been downloaded, it's now time to start the server.

```
# Create a new in-memory serversurreal start --user root --pass secret --allow-all
```

Lastly, use the import command to add the dataset.

Use the command below to import the surreal deal store dataset:

```
surreal import --endpoint http://localhost:8000 --user root --pass secret --ns main --db main surreal-deal-store.surql
```

To import the surreal downloaded the Surreal Deal store (mini) use the command below:

```
surreal import --endpoint http://localhost:8000 --user root --pass secret --ns main --db main surreal-deal-store-mini.surql
```

Please be aware that the import process might take a few seconds.

### Using Curl


First, start the SurrealDB server:

```
# Create a new in-memory serversurreal start --user root --pass secret --allow-all
```

Then download the file and load it into the database:

```
# Download the filecurl -L "https://datasets.surrealdb.com/surreal-deal-store.surql" -o surreal-deal-store.surql# Load the file into the database using the rest endpointcurl -v -X POST -u "root:secret" -H "Surreal-NS: main" -H "Surreal-DB: main" -H "Accept: application/json" --data-binary @surreal-deal-store.surql http://localhost:8000/import
```

If you want to use the mini version:

```
# Download the filecurl -L "https://datasets.surrealdb.com/surreal-deal-store-mini.surql" -o surreal-deal-store-mini.surql# Load the file into the database using the rest endpointcurl -v -X POST -u "root:secret" -H "Surreal-NS: main" -H "Surreal-DB: main" -H "Accept: application/json" --data-binary @surreal-deal-store-mini.surql http://localhost:8000/import
```

### Sample queries


Here are some sample queries you can run on the Surreal Deal Store dataset. We've also included a Surrealist Mini below to help you run these queries.

###### Note


The query results below have been limited to 4 rows for brevity. If you remove the `LIMIT 4` clause from the queries, you'll see the full results.
