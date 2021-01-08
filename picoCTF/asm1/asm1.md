---
title: "Client-side-again"
date: "2021-1-6"
author: "RealFakeAccount"
description: "https://play.picoctf.org/practice/challenge/20"
---

```assembly
asm1:
	<+0>:	push   ebp
	<+1>:	mov    ebp,esp
	<+3>:	cmp    DWORD PTR [ebp+0x8],0x71c
	<+10>:	jg     0x512 <asm1+37>
	<+12>:	cmp    DWORD PTR [ebp+0x8],0x6cf
	<+19>:	jne    0x50a <asm1+29>
	<+21>:	mov    eax,DWORD PTR [ebp+0x8]
	<+24>:	add    eax,0x3
	<+27>:	jmp    0x529 <asm1+60>
	<+29>:	mov    eax,DWORD PTR [ebp+0x8]
	<+32>:	sub    eax,0x3
	<+35>:	jmp    0x529 <asm1+60>
	<+37>:	cmp    DWORD PTR [ebp+0x8],0x8be
	<+44>:	jne    0x523 <asm1+54>
	<+46>:	mov    eax,DWORD PTR [ebp+0x8]
	<+49>:	sub    eax,0x3
	<+52>:	jmp    0x529 <asm1+60>
	<+54>:	mov    eax,DWORD PTR [ebp+0x8]
	<+57>:	add    eax,0x3
	<+60>:	pop    ebp
	<+61>:	ret    
```

You need to learn basic assembly first. 

We can learn from the question that the input is `0x8be`. 

The first branch we will encounter is on `<+3>`. Since `0x8be` is greater than `0x71c`, we jump to `<asm1+37>`.

On `<asm1+37>`, `0x8be` is equal to `0x8be`, so we jump to `<asm1+46>`.

Starting from `<asm1+46>`, we copy `0x8be` into `eax`, then substract `0x3` from `eax`.

We then jump to `<asm+60>`, and reach the end return. `eax` will be the register that store the return value. 

We can learn from previous analysis that when function return , `eax` is `0x8be` - `0x3` = `0x8bb`.