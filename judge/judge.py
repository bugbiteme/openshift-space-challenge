import configparser
import requests
import time
import csv

PASSWORDS = []

config = configparser.ConfigParser()
config.read('settings.ini')

PLAYER_COUNT = 100

def check_url_response(url, message):
    print(url)
    try:
        response = requests.get(url)
        if response.text.strip() == message:
            return True
        else:
            return False
    except requests.RequestException:
        return False


def get_username(player):
    URL = "https://scavenger-ctfd.apps.{}".format(config['DEFAULT']['cluster_domain'])
    username = "admin"
    password = "redhat123"

    s = requests.session()
    s.headers.update({"User-Agent": "curl/7.67.0"})

    # Grab a nonce
    r = s.get(f"{URL}/login")
    if r.status_code != 200:
        raise AuthenticationError(
            f"Received status code {r.status_code} from login get"
        )

    # Parse the nonce
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

    r = s.get(f"{URL}/api/v1/users/{player+1}")
    return (r.json()['data']['name'])

def submit_flag(player, challenge, flag):
    URL = "https://scavenger-ctfd.apps.{}".format(config['DEFAULT']['cluster_domain'])
    username = get_username(player)
    password = PASSWORDS[player]

    s = requests.session()
    s.headers.update({"User-Agent": "curl/7.67.0"})

    # Grab a nonce
    r = s.get(f"{URL}/login")
    if r.status_code != 200:
        raise AuthenticationError(
            f"Received status code {r.status_code} from login get"
        )

    # Parse the nonce
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
    csrf_token = r.text.split("csrfNonce': \"")[1].split('"')[0]

    # Save requests session
    session = s

    # Get user profile
    r = session.get(f"{URL}/api/v1/users/me")
    if r.status_code != 200:
        raise RuntimeError(f"failed to retrieve profile")

    data = r.json()["data"]

    r = session.post(
        f"{URL}/api/v1/challenges/attempt",
        json={"challenge_id": challenge, "submission": flag},
        headers={"CSRF-Token": csrf_token},
    )
    if r.status_code != 200:
        raise RuntimeError("failed to submit flag")

    # Check if it was right
    print(r.json()["data"])

def challenge_3():
    BASE_URL = "https://hello-player{}.apps.{}/"
    while True:
        for i in range(1, PLAYER_COUNT + 1):
            url_to_check = BASE_URL.format(i, config['DEFAULT']['cluster_domain'])
            if check_url_response(url_to_check, "Hello World"):
                submit_flag(i, 4, "FLAG_HELLO_99")

def challenge_4():
    BASE_URL = "https://hello-player{}.apps.{}/"
    while True:
        for i in range(1, PLAYER_COUNT + 1):
            url_to_check = BASE_URL.format(i, config['DEFAULT']['cluster_domain'])
            if check_url_response(url_to_check, "Bonjour Monde"):
                submit_flag(i, 5, "FLAG_BONJOUR_99")

def main():

    global PASSWORDS
    with open("../credentials.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            PASSWORDS.append(row[1])  # Assuming password is the second column

    while True:
        challenge_3()
        challenge_4()

if __name__ == "__main__":
    main()
