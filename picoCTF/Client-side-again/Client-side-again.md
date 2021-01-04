---
title: "Client-side-again"
date: "2020-12-21"
author: "RealFakeAccount"
description: "https://play.picoctf.org/practice/challenge/69?category=1&page=1"
---
You can find a embedded script in the HTML source:

The following js code is formatted using <https://beautifier.io/>

*Note that this js formatting website will delete the declaration of _0x5a46 by default*

```javascript
var _0x5a46 = ["f49bf}", "_again_e", "this", "Password Verified", "Incorrect password", "getElementById", "value", "substring", "picoCTF{", "not_this"];

(function(_0x4bd822, _0x2bd6f7) {
    var _0xb4bdb3 = function(_0x1d68f6) {
        while (--_0x1d68f6) {
            _0x4bd822['push'](_0x4bd822['shift']());
        }
    };
    _0xb4bdb3(++_0x2bd6f7);
}(_0x5a46, 0x1b3));

var _0x4b5b = function(_0x2d8f05, _0x4b81bb) {
    _0x2d8f05 = _0x2d8f05 - 0x0;
    var _0x4d74cb = _0x5a46[_0x2d8f05];
    return _0x4d74cb;
};

function verify() {
    checkpass = document[_0x4b5b('0x0')]('pass')[_0x4b5b('0x1')];
    split = 0x4;
    if (checkpass[_0x4b5b('0x2')](0x0, split * 0x2) == _0x4b5b('0x3')) {
        if (checkpass[_0x4b5b('0x2')](0x7, 0x9) == '{n') {
            if (checkpass[_0x4b5b('0x2')](split * 0x2, split * 0x2 * 0x2) == _0x4b5b('0x4')) {
                if (checkpass[_0x4b5b('0x2')](0x3, 0x6) == 'oCT') {
                    if (checkpass[_0x4b5b('0x2')](split * 0x3 * 0x2, split * 0x4 * 0x2) == _0x4b5b('0x5')) {
                        if (checkpass['substring'](0x6, 0xb) == 'F{not') {
                            if (checkpass[_0x4b5b('0x2')](split * 0x2 * 0x2, split * 0x3 * 0x2) == _0x4b5b('0x6')) {
                                if (checkpass[_0x4b5b('0x2')](0xc, 0x10) == _0x4b5b('0x7')) {
                                    alert(_0x4b5b('0x8'));
                                }
                            }
                        }
                    }
                }
            }
        }
    } else {
        alert(_0x4b5b('0x9'));
    }
}
```

You can see that the code is obfuscated.

Use <http://www.jsnice.org/> to deobfuscate:

```js
'use strict';
/** @type {!Array} */
var _0x5a46 = ["f49bf}", "_again_e", "this", "Password Verified", "Incorrect password", "getElementById", "value", "substring", "picoCTF{", "not_this"];
(function(data, i) {
  /**
   * @param {number} isLE
   * @return {undefined}
   */
  var write = function(isLE) {
    for (; --isLE;) {
      data["push"](data["shift"]());
    }
  };
  write(++i);
})(_0x5a46, 435);
/**
 * @param {string} level
 * @param {?} ai_test
 * @return {?}
 */
var _0x4b5b = function(level, ai_test) {
  /** @type {number} */
  level = level - 0;
  var rowsOfColumns = _0x5a46[level];
  return rowsOfColumns;
};
/**
 * @return {undefined}
 */
function verify() {
  checkpass = document[_0x4b5b("0x0")]("pass")[_0x4b5b("0x1")];
  /** @type {number} */
  split = 4;
  if (checkpass[_0x4b5b("0x2")](0, split * 2) == _0x4b5b("0x3")) {
    if (checkpass[_0x4b5b("0x2")](7, 9) == "{n") {
      if (checkpass[_0x4b5b("0x2")](split * 2, split * 2 * 2) == _0x4b5b("0x4")) {
        if (checkpass[_0x4b5b("0x2")](3, 6) == "oCT") {
          if (checkpass[_0x4b5b("0x2")](split * 3 * 2, split * 4 * 2) == _0x4b5b("0x5")) {
            if (checkpass["substring"](6, 11) == "F{not") {
              if (checkpass[_0x4b5b("0x2")](split * 2 * 2, split * 3 * 2) == _0x4b5b("0x6")) {
                if (checkpass[_0x4b5b("0x2")](12, 16) == _0x4b5b("0x7")) {
                  alert(_0x4b5b("0x8"));
                }
              }
            }
          }
        }
      }
    }
  } else {
    alert(_0x4b5b("0x9"));
  }
}
;
```

We first analyze the first function:

```js
(function(data, i) {
  /**
   * @param {number} isLE
   * @return {undefined}
   */
  var write = function(isLE) {
    for (; --isLE;) {
      data["push"](data["shift"]());
    }
  };
  write(++i);
})(_0x5a46, 435);
```

For those who don't familiar with js, this is called self-invoking function. 
This function have no returns, and it simply shuffle the array `_0x5a46`. The final array can be computed by hands, but you don't need to trouble. you can take advantage of console. Typing `_0x5a46` in your debugger (in F12), you can get the array easily.

```js
/**
 * @param {string} level
 * @param {?} ai_test
 * @return {?}
 */
var _0x4b5b = function(level, ai_test) {
  /** @type {number} */
  level = level - 0;
  var rowsOfColumns = _0x5a46[level];
  return rowsOfColumns;
};
```

Let's anaysis the second function. You can tell that the second parameter, ai_test, is redundant.
Then, this function simply return the string in `_0x5a46` by its index. Again, you can use Debugger to check the result string.

```js
_0x4b5b("0x0") = "getElementById"
_0x4b5b("0x1") = "value"
_0x4b5b("0x2") = "substring"
_0x4b5b("0x3") = "picoCTF{"
_0x4b5b("0x4") = "not_this"
_0x4b5b("0x5") = "f49bf}"
_0x4b5b("0x6") = "_again_e"
_0x4b5b("0x7") = "this"
_0x4b5b("0x8") = "Password Verified"

```

Take these to our final function, and condense some calculation:

```js

/**
 * @return {undefined}
 */
function verify() {
  checkpass = document["getElementById"]("pass")["value"];
  /** @type {number} */
  split = 4;
  if (checkpass["substring"](0, 8) == "picoCTF{") {
    if (checkpass["substring"](7, 9) == "{n") {
      if (checkpass["substring"](8, 16) == "not_this") {
        if (checkpass["substring"](3, 6) == "oCT") {
          if (checkpass["substring"](24, 32) == "f49bf}") {
            if (checkpass["substring"](6, 11) == "F{not") {
              if (checkpass["substring"](16, 24) == "_again_e")) {
                if (checkpass["substring"](12, 16) == _0x4b5b("this")) {
                  alert("Password Verified");
                }
              }
            }
          }
        }
      }
    }
  } else {
    alert("Incorrect password");
  }
}
;
```

Apply the same strategy as "dont-use-client-side", we can get the final flag.
