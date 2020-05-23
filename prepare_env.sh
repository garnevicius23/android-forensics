#!/bin/bash

# Ask for root permissions
if [ $EUID != 0 ]; then
            sudo "$0" "$@"
            exit $?
fi

echo Will update system...
apt update && apt upgrade

echo Installing adb
apt install adb

echo Installing pip3..
apt install python3-pip

echo Installing required python modules..
pip3 install -r ./analyze/requirements.txt
python3 -m pip install --user --upgrade reportlab
