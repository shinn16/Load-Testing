#!/usr/bin/env bash
# This script is meant to be run on the monitor machines. run.sh uses these script to begin monitoring the target machines
# This script is responsible for starting the monitor, collecting the data from it, cleaning the data with the compactor,
# and sending the data back to a data server. A copy of all the data is archived locally in the output folder.
# This script essentially does all the heavy lifting.

if [ "$1" == "-h" ]
then # prints help screen
    echo "Help menu: remoteMonitor.sh"
    echo "Usage: ./remoteMonitor.sh {Web/MySQL/Driver} {yes} {linux/windows} {DS2 config w/o .txt} {Platform (Vbox, VMware, etc)} {Test number}"
else # execute program
    date  # for logging purposes
    # first check to see if we have been given the command line equivalent of yes for config file existance
    if [ "$2" = ""  ]  # this checks to see if we need a manual input
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
    MACHINE_TYPE="$MACHINE"
    MACHINE+="_output.csv"
    echo "configuration: "
    echo "--------------------"
    echo "IP: $IP"
    echo "Username: $USER_NAME"
    echo "Password: $PASSWORD"
    echo "Monitor Commands: $FOLDER"
    echo "Analyze Commands: $ANALYZE"
    echo "Output file: $MACHINE"
    echo "Machine Type: $MACHINE_TYPE"
    echo "OS: $3"
    echo "LoadTest Config: $4.txt"
    echo "--------------------"
    echo "Monitoring $IP..."
    cd ../ # going back a dir to put the output file in the root

    # based on the OS we are monitoring, we use the proper python command
    if [[ $3 == "windows" ]]
    then
        sshpass -p "$PASSWORD" ssh "$USER_NAME"@"$IP" "(python $FOLDER)" > "$MACHINE" # piping output to local machine
    else
        sshpass -p "$PASSWORD" ssh "$USER_NAME"@"$IP" "(python3 $FOLDER)" > "$MACHINE" # piping output to local machine
    fi
    echo "Analyzing Data..."
    python3 Compactor.py $ANALYZE  # for whatever reason, this cannot be put in quotes.
    echo "Done! Preparing to transfer data..."
    NEWEST=$( ls -Art Output | grep "$MACHINE_TYPE" | tail -n 2 )  # gets the 2 newest outputs from the Machine Type
    echo "File to transfer: $NEWEST"


    # setting proper directory based on the OS that is being monitored
    if [[ $3 == "windows" ]]
    then
        sshpass -p @cite123 ssh neo@192.168.1.123 "cd Desktop/LoadTest/; mkdir $4; cd $4; mkdir windows_$5; cd windows_$5; mkdir test$6"
        echo "cd ./Desktop/LoadTest/$4/windows_$5/test$6" > "$MACHINE_TYPE"sftp.txt

    else
        sshpass -p @cite123 ssh neo@192.168.1.123 "cd Desktop/LoadTest/; mkdir $4; cd $4; mkdir linux_$5; cd linux_$5; mkdir test$6"
        echo "cd ./Desktop/LoadTest/$4/linux_$5/test$6" > "$MACHINE_TYPE"sftp.txt

    fi
    # building the transfer script
    for i in $NEWEST  # for the two new files, add an entry for the sftp script
    do
        echo "put ./Output/\"$i\"" >> "$MACHINE_TYPE"sftp.txt
    done
    # end the file
    echo "exit" >> "$MACHINE_TYPE"sftp.txt

    # executing the transfer
    sshpass -p @cite123 sftp -oBatchMode=no -b - neo@192.168.1.123 < "$MACHINE_TYPE"sftp.txt
    echo "Done! All processes finished, exiting"

    # new lines at bottom of log file
    echo ""
    echo ""
fi