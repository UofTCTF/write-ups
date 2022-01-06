---
title: "Notes of pwn.college babysuid levels"
date: "2022-01-04"
author: "uoft-flyfreejay"
description: "short notes for pwn.college dojo's babysuid exercises"
---

# Intro

My first ever write-ups (woohoo)!

This page will have short notes on each level of pwn.college's Program Misues module exercises, babysuid.
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

