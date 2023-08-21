import configparser
import requests
import time
import csv
import concurrent.futures
import random

PASSWORDS = []

config = configparser.ConfigParser()
config.read('settings.ini')

PLAYER_COUNT = 100
MAX_THREADS = 10

morse_messages = {
    "ROOM SERVICE? ORDERED COCONUTS 3 DAYS AGO.",
    "SEND PIZZA. TIRED OF COCONUTS.",
    "YOUR UBER IS ARRIVING NOW. JUST KIDDING.",
    "SEND SUNSCREEN.",
    "FORGOT CHARGER. ANY SPARES?",
    "404: BEACH NOT FOUND. PLEASE REDIRECT.",
    "HELP! MISSING WIFI CODE!",
    "THE FLAG CODE IS: CONTAINERS"
}

morse_dict = {
    "!":"-.-.--",
    "$":"...-..-",
    "&":".-...",
    "'":".----.",
    "(":"-.--.",
    ")":"-.--.-",
    "+":".-.-.",
    "-":"-....-",
    ".":".-.-.-",
    "/":"-..-.",
    "0":"-----",
    "1":".----",
    "2":"..---",
    "3":"...--",
    "4":"....-",
    "5":".....",
    "6":"-....",
    "7":"--...",
    "8":"---..",
    "9":"----.",
    ":":"---...",
    ";":"-.-.-.",
    "=":"-...-",
    "?":"..--..",
    "@":".--.-.",
    "A":".-",
    "B":"-...",
    "C":"-.-.",
    "D":"-..",
    "E":".",
    "F":"..-.",
    "G":"--.",
    "H":"....",
    "I":"..",
    "J":".---",
    "K":"-.-",
    "L":".-..",
    "M":"--",
    "N":"-.",
    "O":"---",
    "P":".--.",
    "Q":"--.-",
    "R":".-.",
    "S":"...",
    "T":"-",
    "U":"..-",
    "V":"...-",
    "W":".--",
    "X":"-..-",
    "Y":"-.--",
    "Z":"--..",
    "_":"..--.-",
    " ":"/"
}

# Function to convert ASCII to Morse code
def ascii_to_morse(input_string):
    return ' '.join([morse_dict.get(char.upper(), '') for char in input_string])

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

def post_json_and_forget(url, data):
    try:
        print(data)
        requests.post(url, json=data)
    except:
        pass  # Ignore exceptions

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

def challenges_4_and_5():
    for i in range(1, PLAYER_COUNT + 1):
        url = "https://hello-player{}.apps.{}/".format(i, config['DEFAULT']['cluster_domain'])
        print(url)
        try:
            response = requests.get(url).text.strip()
            if response == "Hello World":
                submit_flag(i, 4, "FLAG_HELLO_99")
            if response == "Bonjour Monde":
                submit_flag(i, 5, "FLAG_BONJOUR_99")
        except requests.RequestException:
            return False

def challenge_morse():
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for i in range(1, PLAYER_COUNT + 1):
            url = "https://morse-player{}.apps.{}/decode-morse".format(i, config['DEFAULT']['cluster_domain'])
            print(url)
            morse_message = random.choice(list(morse_messages))
            data = {
                'message': ascii_to_morse(morse_message)
            }
            executor.submit(post_json_and_forget, url, data)

def main():

    global PASSWORDS
    with open("../credentials.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            PASSWORDS.append(row[1])

    while True:
        challenge_morse()
        challenges_4_and_5()

if __name__ == "__main__":
    main()
