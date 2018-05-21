#!/usr/bin/env bash
echo "This is the test directory: $1"
DATE=$(date)
DATE=$(echo "$DATE" | sed 's/..:..://p' )
echo "The tests will be stored in: $DATE"
echo "mkdir $1" > sftp.txt
echo "cd $1" >> sftp.txt
echo "mkdir $DATE" >> sftp.txt