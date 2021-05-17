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
