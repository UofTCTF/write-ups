---
title: "Client-side-again"
date: "2021-1-7"
author: "RealFakeAccount"
description: "https://play.picoctf.org/practice/challenge/60"
---

```java
import java.util.*;

class VaultDoor3 {
    public static void main(String args[]) {
        VaultDoor3 vaultDoor = new VaultDoor3();
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter vault password: ");
        String userInput = scanner.next();
	String input = userInput.substring("picoCTF{".length(),userInput.length()-1);
	if (vaultDoor.checkPassword(input)) {
	    System.out.println("Access granted.");
	} else {
	    System.out.println("Access denied!");
        }
    }

    // Our security monitoring team has noticed some intrusions on some of the
    // less secure doors. Dr. Evil has asked me specifically to build a stronger
    // vault door to protect his Doomsday plans. I just *know* this door will
    // keep all of those nosy agents out of our business. Mwa ha!
    //
    // -Minion #2671
    public boolean checkPassword(String password) {
        if (password.length() != 32) {
            return false;
        }
        char[] buffer = new char[32];
        int i;
        for (i=0; i<8; i++) {
            buffer[i] = password.charAt(i);
        }
        for (; i<16; i++) {
            buffer[i] = password.charAt(23-i);
        }
        for (; i<32; i+=2) {
            buffer[i] = password.charAt(46-i);
        }
        for (i=31; i>=17; i-=2) {
            buffer[i] = password.charAt(i);
        }
        String s = new String(buffer);
        return s.equals("jU5t_a_sna_3lpm12g94c_u_4_m7ra41");
    }
}

```

We know how this code modifies our password and we know what we need at end (`jU5t_a_sna_3lpm12g94c_u_4_m7ra41`). So we need to be patient to reverse this process.

For the first 8 characters in buffer (`jU5t_a_s`), they equal to password.charAt(i). so `password[0:8]` = `jU5t_a_s`.

Next, `password[8:16]` = `buffer[15:8-1:-1]` = `1mpl3_an`

Then, `password[16:32:2]` = `buffer[30:16-1:-2]` = `4rm4uc92`

Finally, `password[17:32:2]` = `buffer[17:32:2]` = `g4___7a1`

Join the last 2, we can get `password[16:32]` = `4gr4m_4_u_c79a21`

Combine them, the password is `jU5t_a_s1mpl3_an4gr4m_4_u_c79a21`

Don't forget add picoCTF{} in the final answer.