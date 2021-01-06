---
title: "logon"
date: "2020-12-21"
author: "RealFakeAccount"
description: "https://play.picoctf.org/practice/challenge/46"
---
This website gives us username and password. Looks like a SQL injection question.

But after a few trial, we find that it seems they don't check password at all.

Then we can find that this website store username, password and privilege in cookies.

Thus we can just change the `admin` attribute in cookies to `True`.

Fresh the page, then we can get the flag.