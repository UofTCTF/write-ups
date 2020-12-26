'''
This script is used for https://play.picoctf.org/practice/challenge/29?category=1&page=1

The result array starts with `89 50 4E 47 0D 0A 1A 0A`,
ends with `00 00 00 00 49 45 4E 44 AE 42 60 82`.
'''

PNG_HEADER = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52] # these will transform into oct automatically
PNG_END = [0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82]
BYTES = []
LEN = 16

import base64 as b64
import os
from typing import List

bytes_chunk_num = 0
def check_idx(idx: int, value: str):
    '''
    Given the index and value of one key elements, check if it satisfied the assumption.
    value should be a char, and idx should less than 16
    '''
    flag = True
    shifter = ord(value) - 48 
    
    # check the PNG_HEADER
    # i = idx, j = 0
    flag &= (PNG_HEADER[idx] == BYTES[((shifter * LEN) % len(BYTES)) + idx])
    
    #check the PNG_END
    # i = idx, j = 3
    if 3 < idx < 16:
        flag &= (PNG_END[idx - 4] == BYTES[(((bytes_chunk_num - 1 + shifter) * LEN) + idx) % len(BYTES)])
        
    return flag

mxlen = 0
def dfs(key: List[str]) -> List[str]:
    ans = []
    global mxlen
    mxlen = max(mxlen, len(key))

    assert len(key) < 17
    if len(key) == 16:
        print("".join(key))
        ans.append(key)
        return
    
    for i in range(48, min(122 + 1, 48 + bytes_chunk_num)): # reduce searching range to ascii and number of chucks
        if check_idx(len(key), chr(i)): # choose valid char to continue searching
            key.append(chr(i))
            dfs(key)
            key.pop()

    return

if __name__ == "__main__":
    with open("Java Script Kiddle.txt", 'r') as f:
        for line in f:
            BYTES.append(int(line.strip()))
            
    bytes_chunk_num = int(len(BYTES) / 16);
    
    dfs([])
    #print(mxlen)
    #if len(ans) != 0:
    #    print("possible answers are: {}".format(ans))
    #else: print("No answer found")
    