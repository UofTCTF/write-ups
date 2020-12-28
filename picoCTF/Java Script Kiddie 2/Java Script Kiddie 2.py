'''
This script is used for https://play.picoctf.org/practice/challenge/29?category=1&page=1

The result array starts with `89 50 4E 47 0D 0A 1A 0A`,
MAY ends with `00 00 00 00 49 45 4E 44 AE 42 60 82`.
'''

PNG_HEADER = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52] # these will transform into oct automatically
BYTES = []
LEN = 16

import base64 as b64
import os
from typing import List

bytes_chunk_num = 0
def check_idx(idx: int, value: int):
    '''
    Given the index and value of one key elements, check if it satisfied the assumption.
    value should be a char, and idx should less than 16
    '''
    flag = True
    shifter = value 
    
    # check the PNG_HEADER
    # i = idx, j = 0
    flag &= (PNG_HEADER[idx] == BYTES[((shifter * LEN) % len(BYTES)) + idx])
    
    return flag

ans = []
def dfs(key: List[int]):

    if len(key) == 16:
        global ans
        ans.append("".join([str(i) for i in key]))
        return
    
    for i in range(0, min(100, bytes_chunk_num)): # reduce searching range to 100 and number of chucks
        if check_idx(len(key), i): # choose valid number to continue searching
            key.append(i)
            dfs(key)
            key.pop()

    return

def assemble_png(key: str):
    result = [None] * (LEN * bytes_chunk_num)
    for i in range(0, LEN):
        shifter = ord(key[i]) - 48
        for j in range(0, bytes_chunk_num):
            if (((j + shifter) * LEN) % len(BYTES)) + i > len(BYTES): break
            result[(j * LEN) + i] = BYTES[(((j + shifter) * LEN) % len(BYTES)) + i]

    return bytearray(result)


if __name__ == "__main__":
    with open("Java Script Kiddle 2.txt", 'r') as f:
        for line in f:
            BYTES.append(int(line.strip()))
            
    bytes_chunk_num = len(BYTES) // LEN
    
    dfs([])
    if len(ans) != 0:
       print("possible answers are: {}".format(ans))
    else: print("No answer found")
    
    print("Generating png files...")

    os.mkdir("./pngs")

    for idx in range(0, len(ans)):
        with open("./pngs/{}.png".format(idx), 'wb') as f:
            f.write(assemble_png(ans[idx]))
