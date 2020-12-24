'''
This script is used for https://play.picoctf.org/practice/challenge/29?category=1&page=1

The result array starts with `89 50 4E 47 0D 0A 1A 0A`,
ends with `00 00 00 00 49 45 4E 44 AE 42 60 82`.
'''

PNG_HEADER = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A] # these will transform into oct automatically
PNG_END = [0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82]
BYTES = []
LEN = 16

import base64 as b64
import os
from typing import List

def check_idx(idx: int, value: str):
    '''
    Given the index and value of one key elements, check if it satisfied the assumption.
    value should be a char, and idx should less than 8
    '''
    flag = True
    shifter = ord(value) - 48 

    # check the PNG_HEADER
    # i = idx, j = 0
    if idx < 8:
        flag &= (PNG_HEADER[idx] == BYTES[((shifter * LEN) % len(BYTES)) + idx])

    #check the PNG_END
    # i = idx, j = 44
    if 3 < idx < 16:
        flag &= (PNG_END[((44 * LEN) + idx) - (44 * LEN) - 4] == BYTES[(((44 + shifter) * LEN) % len(BYTES)) + idx])
    
    return flag

mxlen = 0
def dfs(key: List[str]) -> List[str]:
    ans = []
    global mxlen
    mxlen = max(mxlen, len(key))

    assert len(key) < 17
    if len(key) == 16:
        ans.append(key)
        return ans

    for i in range(48, 122 + 1): # ascii
        if check_idx(len(key), chr(i)): # choose valid char to continue searching
            key.append(chr(i))
            ans.extend(dfs(key))
            key.pop()

    return ans

if __name__ == "__main__":
    with open("Java Script Kiddle.txt", 'r') as f:
        for line in f:
            BYTES.append(int(line.strip()))
        assert len(BYTES) == 720

    ans = dfs([])
    print(mxlen)
    if len(ans) != 0:
        print("possible answers are: {}".format(ans))
    else: print("No answer found")
    