import random
import configparser
import requests
from kubernetes import client, config

config_parser = configparser.ConfigParser()
config_parser.read('settings.ini')

PLAYER_COUNT = 100
MAX_THREADS = 16

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
    "!": "-.-.--",
    "$": "...-..-",
    "&": ".-...",
    "'": ".----.",
    "(": "-.--.",
    ")": "-.--.-",
    "+": ".-.-.",
    "-": "-....-",
    ".": ".-.-.-",
    "/": "-..-.",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "?": "..--..",
    "@": ".--.-.",
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "_": "..--.-",
    " ": "/"
}


def ascii_to_morse(input_string):
    return ' '.join([morse_dict.get(char.upper(), '') for char in input_string])


def post_json_and_forget(url, data):
    try:
        requests.post(url, json=data)
    except:
        pass  # Ignore exceptions


def challenge_morse():

    for i in range(1, PLAYER_COUNT + 1):
        url = f"https://morse-player{i}.apps.{config_parser['DEFAULT']['cluster_domain']}/decode-morse"
        morse_message = random.choice(list(morse_messages))
        data = {
            'message': ascii_to_morse(morse_message)
        }
        print(url)
        post_json_and_forget, url, data


def main():
    while True:
        challenge_morse()


if __name__ == "__main__":
    main()
