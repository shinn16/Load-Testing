#!/usr/bin/env bash
# first check to see if we have been given the command line equivalent of yes for config file existance
if [ "$2" = ""  ]  # this checks to see if we need a manaul input
then
    echo "Do you have a config file? y/N"
    read CONFIG
fi
if [ "$CONFIG" = "y" -o "$2" != "" ] #
then
    # get the right config file
    if [ "$1" = "Web" ]
    then
         source "../Config/Web_Config.txt"
    fi

    if  [ "$1" = "MySQL" ]
    then
        source "../Config/MySQL_Config.txt"
    fi

    if [ "$1" = "Driver" ]
    then
        source "../Config/Driver_Config.txt"
    fi
else
  echo "Please enter the IP of the machine you wish to monitor: "
read IP
echo "Please enter the username you wish to run under: "
read USER_NAME
echo "Please enter the password of the user: "
read PASSWORD
echo "What is the directory of the Monitor.py Script?"
read FOLDER
echo "What arguments should be applied to Monitor.py?"
read ARGS
echo "What are the arguments for the analyzer?"
read ANALYZE
echo "What type of machine are you monitoring? MySQL, Web, Driver?"
read MACHINE
fi

FOLDER+="/Monitor.py"
FOLDER+=" $ARGS"
MACHINE+="_output.csv"
echo "configuration: "
echo "--------------------"
echo "IP: $IP"
echo "Username: $USER_NAME"
echo "Password: $PASSWORD"
echo "Monitor Commands: $FOLDER"
echo "Analyze Commands: $ANALYZE"
echo "Output file: $MACHINE"
echo "--------------------"
echo "Monitoring $IP..."
cd ../ # going back a dir to put the output file in the root
sshpass -p "$PASSWORD" ssh "$USER_NAME"@"$IP" "(python3 $FOLDER)" > "$MACHINE" # piping output to local machine
echo "Analyzing Data..."
python3 Compactor.py $ANALYZE  # for whatever reason, this cannot be put in quotes.
echo "Done! Preparing to transfer data..."
NEWEST=( $( ls -Art Output | tail -n 2 ) ) # gets the 2 newest file in the directory
echo "File to transfer: $NEWEST"

# building the transfer script
echo "cd ./Desktop/LoadTest" > sftp.txt
for i in "$NEWEST"
    do
        TRANSFER="./Output/\"$i\"" # getting path to the newest file
        echo "put $TRANSFER" >> sftp.txt
done

echo "exit" >> sftp.txt
# executing the transfer
sshpass -p @cite123 sftp -oBatchMode=no -b - neo@192.168.1.123 < sftp.txt
echo "Done! All processes finished, exiting"