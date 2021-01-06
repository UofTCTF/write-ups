---
title: "Java-Script-Kiddie2"
date: "2020-12-27"
author: "RealFakeAccount"
description: "https://play.picoctf.org/practice/challenge/33
---
```js

var bytes = [];
$.get("bytes", function(resp) {
    bytes = Array.from(resp.split(" "), x => Number(x));
});

function assemble_png(u_in){
    var LEN = 16;
    var key = "00000000000000000000000000000000";
    var shifter;
    if(u_in.length == key.length){
        key = u_in;
    }
    var result = [];
    for(var i = 0; i < LEN; i++){
        shifter = Number(key.slice((i*2),(i*2)+1));
        for(var j = 0; j < (bytes.length / LEN); j ++){
            result[(j * LEN) + i] = bytes[(((j + shifter) * LEN) % bytes.length) + i]
        }
    }
    while(result[result.length-1] == 0){
        result = result.slice(0,result.length-1);
    }
    document.getElementById("Area").src = "data:image/png;base64," + btoa(String.fromCharCode.apply(null, new Uint8Array(result)));
    return false;
}
		
```

WARNING: Please finish `Java Script Kiddle` before starting doing this question.

This question is nearly the same as the previous one, except they use 2 digit for one index.

Luckly, we use a general method to solve `Java Script Kiddle`. Thus, we can solve this one just simply modify our previous code.

Check `Java Script Kiddle 2.py` for the solution code.