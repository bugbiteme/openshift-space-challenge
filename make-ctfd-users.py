import csv
from passlib.hash import bcrypt_sha256
import json
import datetime

def read_csv_file(file_name):
    with open(file_name, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        credentials = [row for row in reader]
    return credentials

def generate_json_output(credentials):
    results = []

    # Admin user data
    admin_data = {
        "id": 1,
        "oauth_id": None,
        "name": "admin",
        "password": bcrypt_sha256.hash("redhat123"),
        "email": "green@redhat.com",
        "type": "admin",
        "secret": None,
        "website": None,
        "affiliation": None,
        "country": None,
        "bracket": None,
        "hidden": 1,
        "banned": 0,
        "verified": 0,
        "team_id": None,
        "created": datetime.datetime.now().isoformat(),
        "language": None
    }
    results.append(admin_data)

    current_id = 2  # Start user ID at 2
    for entry in credentials:
        username = entry["username"]
        plaintext_password = entry["password"]
        hashed_password = bcrypt_sha256.hash(str(plaintext_password))

        user_data = {
            "id": current_id,
            "oauth_id": None,
            "name": username,
            "password": hashed_password,
            "email": f"{username}@example.com",
            "type": "user",
            "secret": None,
            "website": None,
            "affiliation": None,
            "country": None,
            "bracket": None,
            "hidden": 0,
            "banned": 0,
            "verified": 0,
            "team_id": None,
            "created": datetime.datetime.now().isoformat(),
            "language": None
        }
        results.append(user_data)
        current_id += 1

    # Wrap the results in the desired structure
    output = {
        "count": len(results),
        "results": results
    }

    return output

if __name__ == '__main__':
    credentials = read_csv_file('credentials.csv')
    output = generate_json_output(credentials)

    print(json.dumps(output, indent=4))
