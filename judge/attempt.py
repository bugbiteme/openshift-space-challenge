# Test program to submit flag

import requests

def attempt():
    URL = "https://scavenger-ctfd.apps.cluster-sgkjr.sgkjr.sandbox2569.opentlc.com"
    username = "player2"
    password = "4TEhueU5"

    s = requests.session()
    s.headers.update({"User-Agent": "curl/7.67.0"})

    # Grab a nonce
    r = s.get(f"{URL}/login")
    if r.status_code != 200:
        raise AuthenticationError(
            f"Received status code {r.status_code} from login get"
        )

    # Parse the nonce
    print(r.text)
    nonce = r.text.split('name="nonce" type="hidden" value="')[1].split('"')[0]

    # Attempt authentication
    r = s.post(
        f"{URL}/login",
        data={"name": username, "password": password, "nonce": nonce},
    )
    if r.status_code != 200:
        raise AuthenticationError(
            f"received status code {r.status_code} from login post"
        )

    # Grab the CSRF token
    try:
        csrf_token = r.text.split('csrf_nonce = "')[1].split('"')[0]
    except IndexError:
        csrf_token = r.text.split("csrfNonce': \"")[1].split('"')[0]

        # Save requests session
        session = s

        # Get user profile
        r = session.get(f"{URL}/api/v1/users/me")
        if r.status_code != 200:
            raise RuntimeError(f"failed to retrieve profile")

        data = r.json()["data"]

        print(data)

        r = session.post(
            f"{URL}/api/v1/challenges/attempt",
            json={"challenge_id": 1, "submission": "3"},
            headers={"CSRF-Token": csrf_token},
        )
        if r.status_code != 200:
            raise RuntimeError("failed to submit flag")

        # Check if it was right
        print(r.json()["data"])

if __name__ == '__main__':
    attempt()
