#!/bin/bash

# File to store the generated htpasswd entries
HTPASSWD_FILE="players.htpasswd"

# File to store the player and password pairs
CREDENTIALS_FILE="credentials.csv"

# Start a new credentials file
echo "username,password" > $CREDENTIALS_FILE

# Loop to generate 100 players
for i in $(seq 1 100); do
  # Generate random 8 character password
  PASSWORD=$(cat /dev/urandom | tr -dc 'a-hj-km-np-zA-HJ-KM-NP-Z2-9' | head -c 8)

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

latex credential-handouts.tex
dvipdf credential-handouts.dvi
