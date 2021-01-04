---
title: "Irish-Name-Repo-3"
date: "2020-12-26"
author: "RealFakeAccount"
description: "https://play.picoctf.org/practice/challenge/8?category=1&page=1"
---
Reading through the question. They remove the `username` field. Moreover, we can't see the sql query now.

After a few failed attempts, we know that we have to look for some information.

Firstly, the hints of the question tells us that "Seems like the password is encrypted."

Secondly, we can notice a "debug" parameter in the html source.

Change the debug value to 1 and send the payload `' or '1' = '1`, we can get following:

```sql
SELECT * FROM admin where password = '' be '1' = '1'
```

We can see that `or` is encrypted to `be`. Obviously, this is `ROT13` (also called [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher))

We can then construct our final payload `' be '1' = '1`, which give us:

```sql
SELECT * FROM admin where password = '' or '1' = '1'
```

and get the flag.