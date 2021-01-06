---
title: "Insp3ct0r"
date: "2020-12-21"
author: "RealFakeAccount"
description: "https://play.picoctf.org/practice/challenge/18
---
The description said we should inspect the website code.

Press F12, in the elements with `id="tababout"` attribute, you can find the following:

```html
<!-- Html is neat. Anyways have 1/3 of the flag: picoCTF{tru3_d3 -->
```

Look around, The 2/3 part is in `mycss.css`:

```css
/* You need CSS to make pretty pages. Here's part 2/3 of the flag: t3ct1ve_0r_ju5t */
```

The 3/3 is in `myjs.js`. Note that you may get a 304 status for the js link so it won't load in browser debugger. You need to download manually (with wget, for example).

```javascript
/* Javascript sure is neat. Anyways part 3/3 of the flag: _lucky?2e7b23e3} */
```

Combining them, we can get the final flag.