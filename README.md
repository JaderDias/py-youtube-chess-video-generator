This project does the following

create_db.py

* Downloads a list of chess games in PGN format
* Saves them to a local SQLite database

main.py

* Reads one chess game from the local SQLite database
* Generates images for each board position in the game
* Generates an audio narration for each move using Google Text to Speech API
* Assembles the images and audio together into a videofile
* Uploads the videofile to Youtube

Instructions

* sudo apt install python3-pip
* pip install -r requirements.txt
* python3 create_db.py
* create and dowload a Service Account JSON key from https://console.cloud.google.com/iam-admin/serviceaccounts
* modify main.py to point to this filegit
* create and download a OAuth 2.0 Client ID from https://console.cloud.google.com/apis/credentials
* modify Secrets.py to point to this file
* run main.py