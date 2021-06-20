---
title: "Notes of HTB Machine Labs"
date: "2021-05-12"
author: "RealFakeAccount"
description: "short notes for HTB Machine Lab"
---

# Intro

I usually watch [IppSec's video](https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA) after finishing or failed on one box.
I would often learn some new things in his excellent video. Therefore, I need a place to store the things I learnt.

This article may contains short write-ups, but they won't be detailed. If a detailed write-up is needed, I would open a new article for it.

## Machine Labs

### Blue

- short write-ups

Box for script kiddie like me. Learn [nmap](https://nmap.org/) and [metasploit](https://www.metasploit.com/) and you should be able to solve it in a few minutes.

- what I learnt

```bash
nmap --script=vuln
```

This nmap command could detect vulnerabilities in server. It may take some time.

### Legacy

- short write-ups

nmap could scan the vulnerabilities. Use metasploit to get a reverse shell.

### Lame

- short write-ups

nmap didn't give vulnerabilities this time. However, both server running on this box (vsftpd 2.3.4 and Samba 3.0.20-Debian) is vulnerable. Either of them is in metasploit.

### Jerry

- short write-ups

Credential guessing box. the status panel's credential is `admin:admin` and the manage panel's credential is the default `tomcat:s3cret`. In the manage panel you can upload a JSP reverse shell.

- what I learnt

1. You could use Hydra to crack the password if you can't guess it.

2. You could use `msfvenom` to generate payload.

3. You can use `exploit/multi/handler` to handle the payload you uploaded.

### Netmon

- short write-ups

Search google and you can find Netmon Remote Code Execution vulnerability and Netmon used to save passwords in plain text.
Also find that the FTP config support anonymous login. Therefore, use FTP to extract the old credientials, guess the new one (note that the config was created in 2019), then use metasploit to get a shell.

- notice

The `programdata` is actually a hided folder. You need to use `ls -a` in order to list this folder.

```bash
ftp> ls
200 PORT command successful.
125 Data connection already open; Transfer starting.
02-03-19  12:18AM                 1024 .rnd
02-25-19  10:15PM       <DIR>          inetpub
07-16-16  09:18AM       <DIR>          PerfLogs
02-25-19  10:56PM       <DIR>          Program Files
02-03-19  12:28AM       <DIR>          Program Files (x86)
02-03-19  08:08AM       <DIR>          Users
02-25-19  11:49PM       <DIR>          Windows
226 Transfer complete.
ftp> ls -a
200 PORT command successful.
125 Data connection already open; Transfer starting.
11-20-16  10:46PM       <DIR>          $RECYCLE.BIN
02-03-19  12:18AM                 1024 .rnd
11-20-16  09:59PM               389408 bootmgr
07-16-16  09:10AM                    1 BOOTNXT
02-03-19  08:05AM       <DIR>          Documents and Settings
02-25-19  10:15PM       <DIR>          inetpub
05-12-21  06:53AM            738197504 pagefile.sys
07-16-16  09:18AM       <DIR>          PerfLogs
02-25-19  10:56PM       <DIR>          Program Files
02-03-19  12:28AM       <DIR>          Program Files (x86)
02-25-19  10:56PM       <DIR>          ProgramData
02-03-19  08:05AM       <DIR>          Recovery
02-03-19  08:04AM       <DIR>          System Volume Information
02-03-19  08:08AM       <DIR>          Users
02-25-19  11:49PM       <DIR>          Windows
226 Transfer complete.
```

- what I learnt

1. Use `grep -B5 -A5 pattern` to quick extract the context.

### Granny

- short write-ups

Experience some strange issues using metasploit 6.0.43. MS14-058 wouldn't work. Will come back later.

- what I learnt

1. local_exploit_suggester in metasploit could suggest exploit.

### Bashed

- short write-ups

Use enumeration (Wfuzz or gobuster, for example) to find the location of the php reverse shell that mentioned in the box's website, then notice that sudo allows you to run as another user, so generate a reverse shell and start bash as the new user. Next, find that the root use crontab to execute the scripts of the new user. Modify the scripts to get a shell as root.

- what I learnt

1. <https://github.com/rebootuser/LinEnum> is a good way to quickly explore interesting file in Linux
2. `-s` option of sudo could start an interaction shell. However, it requires password. Use `sudo -u user /bin/bash` instead.
3. CherryTree is a good way to organize information

### Optimum

- short write-ups

metasploit all the way down.

### ScriptKiddie

Finished. Waiting for retirement.

### Blocky

- short write-ups

gobuster could find a /wiki page and a /plugins page, which indicates the files in /plugins may be important. RE the jar file found in the /plugins gives us a password. Notice that althought this password have a username of `root`, it is actually `notch`'s. Notch got sudo privilege and we got his password, thus we can get root shell using sudo.

- what I learnt

1. Don't dig too deep into one finding. Do a throughout information first.

### Delivery

Finished. Waiting for retirement.

### Devel

- short write-ups

Use ftp anonymous to upload a aspx reverse shell.

- what I learnt

1. Metasploit reverse shell handler sometimes wrongly recognize the system. The reverse shell generated by powershell was recognized as BSD. Strange issue.

### Spectra

Finished. Waiting for retirement.

- what I learnt

1. `chmod +s` makes the file run as the user/group who created it.

### Armageddon

Finished. Waiting for retirement.

### Mirai

- short write-ups

Gobuster can find the admin panel. The login page will inform you that this is a newly installed raspberry-pi. Use the default login credentials to login through ssh and get user flag. Finally use `strings` to find the root flag.

- what I learnt

1. disks could be directly `cat`ed as binary. For example, you could `cat /dev/sda`.

### Shocker

- short write-ups

User: shellshock

Root: user could run perl as root. Use perl to spawn a reverse shell.

- what I learnt

1. `gobuster` has a very strange issue. it won't automatically add / after wordlist. Thus in this machine, you can't get the `/cgi-bin/` dir using `gobuster`. `/cgi-bin/` is 403 while `/cgi-bin` is 404.

2. ShellShock

### Sense

- short write-ups

User: there is a file `system-users.txt` tells you the username. Use the default pfsense password to login. Then use CVE to get reverse shell.

Root: reverse shell runs as root.

- what I learnt

1. if you stucked, buster the dir with common file extension (txt, php, pl, py, etc)

### Beep

- short write-ups

User: the webapp `elastix` had a LFI CVE. Use it to extract the config file. It contains the root passwd for ssh.

Root: reverse shell runs as root.

btw, other ways are possible for this machine. For example, this machine is vulnerable to shellshock.

### Nibbles

- short write-ups

User: find nibbleblog and its admin panel. `guess` the password `nibbles` and login as admin (lol). Use CVE to get shell.

Root: user could run all command as root using sudo.

- what I learnt

1. Often, if HTB wants you to guess passwords, it is usually machine name, `password`, `admin`.

### Buff

- short write-ups

User: The website uses unpatched framework. Use script from searchsploit to get shell.

Root: Find there is a vulnerable service `CloudMe`. Use script from searchsploit to get shell.

- what I learnt

1. if the target don't have ssh and you need a tunnel, `chisel` is a good choice.
    Simple usage: 
    ```bash
    server(attack box): ./chisel server -p 8000 --reverse
    client(victim box): ./chisel client 10.10.14.20:8000 R:port:localhost:port
    ```

2. Use `netstat -an` to see the open ports and use `tasklist /v | findstr <portnumber>` to check the process using the port

3. About `msfvenom` payloads: `windows/meterpreter_reverse_tcp` is a quite large reverse shell, while ` windows/meterpreter/reverse_tcp` contains just enough code to connect back to the attacker.

4. If you want to check the privilege of one process, you can use [accesschk](https://docs.microsoft.com/en-us/sysinternals/downloads/accesschk).

### Bank

- short write-ups

Users: set hosts file to `bank.htb` based on info from port 53. use Buster to find `/balance-transfer/`. One file in this folder didn't encrypt. Use the credential in this file to login the panel. the source code of the panel tell us we can upload a php use `.htb` suffix. Upload one and get a user shell.

Root: 2 ways. Either add a new credential in `/etc/passwd`, or use `/var/htb/bin/emergency`, which directly give you a root shell..

- what I learnt

1. In bash, single quote wouldn't inteprete anything while double quote would. So if you want to echo something contain special character ($ for example), use single quote.


2. You can use openssl to [generate hash](https://unix.stackexchange.com/questions/81240/manually-generate-password-for-etc-shadow) for [/etc/shadow](https://www.cyberciti.biz/faq/understanding-etcpasswd-file-format/). In exploit, `-1` is usually enough (which is a MD5).


3. You can use `find -perm -mode` or `find -perm /mode` to [find files with given permission](https://askubuntu.com/questions/829716/diffrence-between-perm-mode-perm-mode-in-find-command). In this question, use
```bash
find / -type f -user root -perm -4000 2>/dev/null
```
to find the emergency file.

### Celestial

- short write-ups

User: Nodejs deserialization exploit. <https://opsecx.com/index.php/2017/02/08/exploiting-node-js-deserialization-bug-for-remote-code-execution/>

Root: Notice the `script.py` in /home/sun/Documents is crontabed by root. Modify it to generate a reverse shell from root.

