---
title: "where-are-the-robots"
date: "2020-12-21"
author: "RealFakeAccount"
description: "https://play.picoctf.org/practice/challenge/4"
---

Robots is an explict hint.

[Introduction to robots.txt](https://developers.google.com/search/docs/advanced/robots/intro)

We should definitely check it as a CTF player. 

Here is the robots.txt file of our target website:

```html
User-agent: *
Disallow: /1bb4c.html
```

You can find your flag in this "Disallow" location.
