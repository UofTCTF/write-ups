This is a learning-solving question.

Both website and hint tell us to look up JWT. 

After searching `JWT vulnerabilities` in Google, you can find this:

<https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/>

But after implementing this method, it seems wrong. When you Change the cookies to 

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VyIjoiYWRtaW4ifQ
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
```

You only get an 500 error.
