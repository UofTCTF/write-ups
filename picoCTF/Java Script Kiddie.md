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
The result array starts with `89 50 4E 47 0D 0A 1A 0A`,
ends with `00 00 00 00 49 45 4E 44 AE 42 60 82`.