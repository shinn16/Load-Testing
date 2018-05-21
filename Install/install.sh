#!/usr/bin/env bash
echo "Is this the machine to monitor(1) or the monitor(2)? 1/2"
read TYPE
if [ "$TYPE" = 1 ]
then
    echo "Installing python3-pip"
    echo "This script was designed to be run on a Debian based machine, you will need to manually install pip if this is not a debian machine."
    sudo -S apt-get install -y python3-pip
    echo "Running python-pip3 to install requirements"
    pip3 install -r requirements.txt
else
    echo "Installing ssh tools"
    sudo -S apt-get install -y python3-pip sshpass
    echo "Running python-pip3 to install requirements"
    pip3 install -r requirements.txt
    echo "Creating config file..."
    python3 CreateConfig.py
fi

echo "If no errors popped up, you should be good to go!"