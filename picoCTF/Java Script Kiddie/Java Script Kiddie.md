```js
var bytes = [];
$.get("bytes", function(resp) {
    bytes = Array.from(resp.split(" "), x => Number(x));
});

function assemble_png(u_in){
    var LEN = 16;
    var key = "0000000000000000";
    var shifter;
    if(u_in.length == LEN){
        key = u_in;
    }
    var result = [];
    for(var i = 0; i < LEN; i++){
        shifter = key.charCodeAt(i) - 48;
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

This blog explains very well:

<https://medium.com/@radekk/picoctf-2019-writeup-for-js-kiddie-7af4f0a20838>


I want to mention some points: first, how to find first 16 bytes of PNG directly from definition.

<https://en.wikipedia.org/wiki/Portable_Network_Graphics>

We can see that the 8-byte signature of PNG is fixed: `0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A` 

The first chunk should always be `IHDR`, and this chunk should always have a `header`, which is Length and Chunk type. 

Luckly, we know both values. Length of `IHDR` is 13 bytes (the image's width (4 bytes); height (4 bytes); bit depth (1 byte, values 1, 2, 4, 8, or 16); color type (1 byte, values 0, 2, 3, 4, or 6); compression method (1 byte, value 0); filter method (1 byte, value 0); and interlace method (1 byte, values 0 "no interlace" or 1 "Adam7 interlace") (13 data bytes total)). Chunk type is 4 ascii bytes represent `IHDR`.

Thus, the header should always be `0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52`.

I want to also mention why you cannot use `IEND` chunk to calculate your key. Because by definition, the data field of the `IEND` chunk can has 0 bytes. Thus, we don't know exactly where `IEND` chunk is until we have calculated out the key. This means we cannot use `IEND` chunk to check the correctness of the key.

For example, these are the end bytes in my result png file:

```
000002b0  7e 28 c2 28 8a c2 00 00  00 00 49 45 4e 44 ae 42  |~(.(......IEND.B|
000002c0  60 82 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |`...............|
```

You can see that `IEND` is followed by 0s, so it is not at "exactly" the end.

You can check my python file `Java Script Kiddie.py` to see how I use dfs to calculate the key.