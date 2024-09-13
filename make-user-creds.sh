#!/bin/bash

# File to store the generated htpasswd entries
HTPASSWD_FILE="players.htpasswd"

# File to store the player and password pairs
CREDENTIALS_FILE="credentials.csv"

# Start a new credentials file
echo "username,password" > $CREDENTIALS_FILE

# Loop to generate 400 players
for i in $(seq 1 400); do
  # Generate random 8 character password
  PASSWORD=$(python -c "import random; import string; \
    print(''.join(random.choice(string.ascii_letters + string.digits) \
    for _ in range(8)))")

  # Append to the htpasswd file
  if [ "$i" -eq 1 ]; then
    echo -n "$PASSWORD" | htpasswd -ciB $HTPASSWD_FILE player$i
  else
    echo -n "$PASSWORD" | htpasswd -iB $HTPASSWD_FILE player$i
  fi

  # Append to the credentials file
  echo "player$i,$PASSWORD" >> $CREDENTIALS_FILE
done

python make-gitea-passwords.py

pdflatex credential-handouts.tex
