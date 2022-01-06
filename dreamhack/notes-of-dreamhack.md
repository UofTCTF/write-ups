---
title: "Notes of dreamhack wargames"
date: "2022-01-06"
author: "uoft-flyfreejay"
description: "short notes for wargames hosted on dreamhack.io"
---

# Intro

This page will have my short notes on wargame challenges I have solved on dreamhack.io.

I really enjoy learning on this platform as it covers various topics from beginner level and has its own learning module. So the types of wargame challenges I will be playing here will vary in genres. 

As the main aim dreamhack.io is to educate new hackers, they provide the players with source codes that are used in the systems of each challenge to analyze them and exploit them accordingly. 

Let's get hacking <3! 

## Web-Hacking

### session

- short write-ups

This wargame is an excellent introductory challenge about cookies & sessions. If you connect to the wargame, you will see a plain webpage that does not have much except for the login button at the top right corner. 

However, looking at the source code of the page reveals more fun things. It seems that the code checks your cookie called `sessionid` and see if the value of that cookie exists in the session storage. If so, it will log you in to the according user. That means that if we know the session value for the `admin` user, we can log in as the admin! 

At the bottom of the source code, the code actually sets the admin's session value to a random `os.urandom(1).hex())`. This will only cover the hex values from 00~FF, which is very brute forcable. 

So let's fire up the burpsuite and forward request to intruder. I won't get into to the details of how to use burpsuite to bruteforce here. If the request length differs from other bruteforce trials, that means we got something. 

I was lucky this time because the session id happened to be '02' for me. Changing the `sessionid` cookie value on the page to '02' and reloading will give me the flag! 

- what I learnt

1. Burpsuite's Intruder to bruteforce through requests

2. what `os.urandom()` does

3. The idea of session hijacking technique

