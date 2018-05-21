#! /usr/bin/env bash
if [ "$1" == "-h" ]
then
    echo "Help menu: update.sh"
    echo "Usage: ./update.sh {list of ip to update separated by space}"
else
    # creating the zip archive
    zip -rq monitor.zip ../../monitor
    for var in "$@" # for all of the parameters given to the script
    do
        echo "Updating on: $var" # move a copy of the zip folder there
        sleep 1
        sshpass -p @cite123 sftp -oBatchMode=no -b - neo@"$var" < ./sftpScripts/update.txt
        sshpass -p @cite123 ssh neo@"$var" "(rm -r monitor; unzip -q monitor.zip; rm monitor.zip)"
    done
    rm monitor.zip
fi