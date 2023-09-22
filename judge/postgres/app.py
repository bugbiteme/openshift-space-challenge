import requests
import os
import time
import csv
from kubernetes import client, config
import urllib3

urllib3.disable_warnings()

PLAYER_COUNT = 100
PASSWORDS = []
successful_flags = []
running_pods = []

cluster_domain = os.environ.get('CLUSTERDOMAIN', '')
token = os.environ.get('JUDGE_SA_TOKEN', '')


def get_username(player):
    URL = f"https://island-ctfd.apps.{cluster_domain}"
    username = "admin"
    password = "redhat123"

    s = requests.session()
    s.headers.update({"User-Agent": "curl/7.67.0"})

    # Grab a nonce
    r = s.get(f"{URL}/login")
    print(r)
    if r.status_code != 200:
        raise Exception(
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
        raise Exception(
            f"received status code {r.status_code} from login post"
        )

    r = s.get(f"{URL}/api/v1/users/{player+1}")
    return (r.json()['data']['name'])


def submit_flag(player, challenge, flag):
    URL = f"https://island-ctfd.apps.{cluster_domain}"
    username = get_username(player)
    password = PASSWORDS[player]

    s = requests.session()
    s.headers.update({"User-Agent": "curl/7.67.0"})

    # Grab a nonce
    r = s.get(f"{URL}/login")
    if r.status_code != 200:
        raise Exception(
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
        raise Exception(
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


# Function to list all running pods
def list_all_running_pods():

    # Define your OpenShift API server URL, namespace, resource type, and resource name
    api_server_url = f'https://api.{cluster_domain}:6443'
    
    # Define the OpenShift API endpoint
    api_url = f'{api_server_url}/api/v1/pods'
    
    # Define the headers with the authentication token
    headers = {
        "Authorization": f"{token}",
        "namespace": "",
        "Content-Type": "application/json"

    }

    # Define query parameters to filter running pods
    params = {
        "fieldSelector": "status.phase=Running"
    }

    running_pods = {}

    # Make a GET request to list running pods
    response = requests.get(api_url, headers=headers, params=params, verify=False)  # Use verify=False to ignore SSL certificate verification (not recommended for production)

    # Check if the request was successful
    if response.status_code == 200:
        pods_data = json.loads(response.text)

        # Print the names of running pods
        for pod in pods_data["items"]:
            namespace = pod["metadata"]["namespace"]
            name = pod["metadata"]["name"]
            phase = pod["status"]["phase"]
            container_statuses = pod["staus"]["container_statuses"]
            print(f"Namespace: {namespace}, Name: {name}")
            if phase == "Running":
                if namespace not in running_pods:
                    running_pods[namespace] = []
                running_pods[namespace].append({
                'pod_name': name,
                'replicas': len(container_statuses) if container_statuses else 0
            })

    return running_pods

# Challenge 13 logic
def challenge_13_postgres():

    all_pods = list_all_running_pods()

    for i in range(1, PLAYER_COUNT + 1):
        print(f"checking if any pods from player{i} starts with postgresql-*")
        time.sleep(0.1)
        if i not in successful_flags:
            namespace_name = f"player{i}"
            if namespace_name in all_pods:
                for pod in all_pods[namespace_name]:
                    print(f"{pod['pod_name']}")
                    if pod['pod_name'].startswith("postgresql-"):
                        submit_flag(i, 13, "FLAG_POSTGRES_99")
                        successful_flags.append(i) 
        else:
                print(f"Flag for player{i} already submitted." )                

def main():
    
    global PASSWORDS
    with open("credentials.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            PASSWORDS.append(row[1])
            
    while True:
        challenge_13_postgres()

if __name__ == "__main__":
    main()
