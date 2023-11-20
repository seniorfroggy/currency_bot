#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt install python3-virtualenv
virtualenv venv -p python3
source venv/bin/activate
export BOT_TOKEN=$1
pip install -r requirements.txt
chmod +x main.py
python3 main.py