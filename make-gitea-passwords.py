import csv

with open('credentials.csv', 'r') as csv_file, open('gitea-set-passwords.sh', 'w') as script_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        username = row['username']
        password = row['password']
        line = f'./gitea --config conf/app.ini admin user create --username {username} --password {password} --email {username}@example.com --must-change-password=false\n'
        print(line)
        script_file.write(line)
