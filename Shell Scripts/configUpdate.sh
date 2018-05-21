#!/usr/bin/env bash
if [ "$1" == "-h" ]
then
    echo "Help menu: configUpdate.sh"
    echo "Usage: ./configUpdate.sh {ip of monitor to update config files} {Optional: absolute path to config folder}"
    echo "-----------------------------------------------------------------------------------------------------------"
    echo "By default, the config folder of the local monitor folder will be used to update the config folder of the"
    echo "remote monitor. This behavior can be changed by adding an optional path to a folder containing the desired"
    echo "config files to be uploaded to the remote monitor."
else
    echo "Updating Config Files on: $1" # move a copy of the zip folder there
    if [[ "$2" != "" ]]
    then # send the specified directory
        holder=($( echo "$2" | sed 's/\// /g' )) # turns the path into an array so we can get the folder names
        zip -rq Config.zip "$2"
        sshpass -p @cite123 sftp -oBatchMode=no -b - neo@"$1" < ./sftpScripts/configUpdate.txt
        sshpass -p @cite123 ssh neo@"$1" "(unzip -q Config.zip; cd monitor; rm -r Config; mv .."$2" ./; mv ${holder[-1]} Config; cd ../; rm -r Config.zip ${holder[0]})"
    else # send the default folder
        zip -rq Config.zip ../Config
         sleep 1
        sshpass -p @cite123 sftp -oBatchMode=no -b - neo@"$1" < ./sftpScripts/configUpdate.txt
        sshpass -p @cite123 ssh neo@"$1" "(unzip -q Config.zip; cd monitor; rm -r Config; mv ../Config ./; cd ../; rm Config.zip)"
    fi
    rm Config.zip
fi