import csv

with open('credentials.csv', 'r') as csv_file, open('gitea-set-passwords.sh', 'w') as script_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        username = row['username']
        password = row['password']
        line = f'./gitea --config conf/app.ini admin user change-password -u {username} -p {password}\n'
        script_file.write(line)
