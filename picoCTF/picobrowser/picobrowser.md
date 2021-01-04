---
title: "picobrowser"
date: "2020-12-22"
author: "RealFakeAccount"
description: "https://play.picoctf.org/practice/challenge/9?category=1&page=1"
---
Use your favorite methods to change the request header.

1.  use proxy tools such as Burp Suite, Wireshark, Fiddler, etc.
2.  use programming languages or tools to send request with your own header.

I love `wget` more, so this is what I did:

```bash
wget --header="User-Agent: picobrowser" https://jupiter.challenges.picoctf.org/problem/28921/flag
```
