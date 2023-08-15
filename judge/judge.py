import requests
import time

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

def submit_flag(player, challenge):
    # Placeholder to submit flag
    print("submit flag")

def challenge_3():
    BASE_URL = "https://hello.player{}.apps.ocp.example.com"
    while True:
        for i in range(1, PLAYER_COUNT + 1):
            url_to_check = BASE_URL.format(i)
            if check_url_response(url_to_check, "Hello World!"):
                submit_flag(url_to_check)

def challenge_4():
    BASE_URL = "https://hello.player{}.apps.ocp.example.com"
    while True:
        for i in range(1, PLAYER_COUNT + 1):
            url_to_check = BASE_URL.format(i)
            if check_url_response(url_to_check, "Bonjour Monde!"):
                submit_flag(url_to_check)

def main():
    while True:
        challenge_3()
        challenge_4()

if __name__ == "__main__":
    main()
