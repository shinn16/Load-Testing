#!/usr/bin/env bash
# This script is meant to be run from a machine that is not the monitor. This script has the ability
# to automate the entire load testing process when used in conjunction with crontabs, a cronjob utility for Linux.
# This script relies on a monitor machine to run the monitor script on various machines. All this script does is trigger
# the automatic start of the load test.

if [ $1 == "-h" ]
then
    echo "Help menu: run.sh"
    echo "Usage: ./run.sh {seconds to delay before load testing} {windows/linux} {DS2 config File w/o .txt} {Platform (VMware, Vbox, etc)} "
else
    # getting the test number
    source "/home/neo/monitor/Shell Scripts/Config/num.txt"
    num=$(expr "$num" + 1)

    # generating a unique log file name for the execution log
    fileStamp=$(date +%d-%m-%y_%H:%M:%S)
    fileStamp+="_Execution.log"

    echo "$(date +%d-%m-%y_%H:%M:%S)"
    echo "---------------------------------------------------------------------------------------------------------------------"
    echo "Please be sure to SSH into the monitor from this machine before executing this script, it will not work otherwise"
    echo "The monitor will also need to have been ssh'd into the machines it needs to monitor."
    echo "---------------------------------------------------------------------------------------------------------------------"
    echo ""
    echo "Configuration:"
    echo "---------------------------------------------------------------------------------------------------------------------"
    echo "Target OS: $2"
    echo "DS2 Config File: $3"
    echo "Platform: $4"
    echo "Test Number: $num"
    echo "Execution Log: $fileStamp"
    echo "---------------------------------------------------------------------------------------------------------------------"
    sleep 2
    echo "Start:"

    # beginning the test
    if [[ $2 == "windows" ]]
    then # windows commands
        # clean the database from the last run
        echo "Cleaning the database from the last run..."
        sshpass -p @cite123 ssh neo@192.168.1.136 "net stop MySQL57 && net start MySQL57 & cd \ds2\mysqlds2\build & mysql -u web --password=web < mysqlds2_cleanup_10mb.sql"

        # cleaning out the tomcat logs
        echo "Removing tomcat logs..."
        sshpass -p @cite123 ssh neo@192.168.1.135 "net stop tomcat6 & cd \\\"Program Files\"\\\"Apache Software Foundation\"\\\"Tomcat 6.0\"\logs & echo Y | del * & net start tomcat6"

        # start the monitors
        echo "Starting the monitors."
        sshpass -p @cite123 ssh neo@192.168.1.107 "(cd ~/monitor/Shell\ Scripts/; ./remoteMonitor.sh Web yes windows $3 $4 $num >> ./Logs/Web_log.txt 2>&1 &)"
        sshpass -p @cite123 ssh neo@192.168.1.107 "(cd ~/monitor/Shell\ Scripts/; ./remoteMonitor.sh MySQL yes windows $3 $4 $num >> ./Logs/MySQL_log.txt 2>&1 &)"
        sshpass -p @cite123 ssh neo@192.168.1.107 "(cd ~/monitor/Shell\ Scripts/; ./remoteMonitor.sh Driver yes windows $3 $4 $num >> ./Logs/Driver_log.txt 2>&1 &)"

        echo "Load test will begin at the end of the countdown"
        for (( i=$1; i > 0; --i ))
        do
            echo "$i..."
            sleep 1
        done

        echo "Starting the load..."
        sshpass -p @cite123 ssh neo@192.168.1.137 "(cd \ds2\drivers & ds2webdriver.exe --config_file=..\\$3.txt)" > "$fileStamp"
        echo "Load test finished, please wait for the ramp down..."
        for (( i=$1; i > 0; --i ))
        do
            echo "$i..."
            sleep 1
        done
        echo "Done!"

    else # Linux Commands
        #cleaning up the previous database entries
        echo "Cleaning the database from the last run..."
        sshpass -p @cite123 ssh -t neo@192.168.1.131 "(echo \"@cite123\" | sudo -S service mysql reload;cd /ds2/mysqlds2/build; mysql -u web --password=web < mysqlds2_cleanup_10mb.sql)"
        sleep 5 # this is a fix for ubuntu, the output from this command is not shown, so there is not delay. This
        # ensures there is a delay before the monitor starts so that the db has time to clear

        # cleaning out the tomcat logs
        echo "Removing tomcat logs..."
        sshpass -p @cite123 ssh neo@192.168.1.130 "(/opt/tomcat6/bin/shutdown.sh; cd /opt/tomcat6/logs; rm * ;/opt/tomcat6/bin/startup.sh)"
        sleep 5

        # start the monitors
        echo "Starting the monitors."
        sshpass -p @cite123 ssh neo@192.168.1.103 "(cd ~/monitor/Shell\ Scripts/; ./remoteMonitor.sh Web yes linux $3 $4 $num >> ./Logs/Web_log.txt 2>&1 &)"
        sshpass -p @cite123 ssh neo@192.168.1.103 "(cd ~/monitor/Shell\ Scripts/; ./remoteMonitor.sh MySQL yes linux $3 $4 $num >> ./Logs/MySQL_log.txt 2>&1 &)"
        sshpass -p @cite123 ssh neo@192.168.1.103 "(cd ~/monitor/Shell\ Scripts/; ./remoteMonitor.sh Driver yes linux $3 $4 $num >> ./Logs/Driver_log.txt 2>&1 &)"

        echo "Load test will begin at the end of the countdown"
        for (( i=$1; i > 0; --i ))
        do
            echo "$i..."
            sleep 1
        done

        echo "Starting the load..."
        sshpass -p @cite123 ssh neo@192.168.1.132 "cd /ds2/drivers; ./ds2webdriver.exe --config_file=../$3.txt" > "$fileStamp"
        echo "Load test finished, please wait for the ramp down..."
        for (( i=$1; i > 0; --i ))
        do
            echo "$i..."
            sleep 1
        done
        echo "Done!"
    fi
    echo "Moving execution log to proper directory..."
    mv ./"$fileStamp" ~/Desktop/LoadTest/"$3"/"$2_$4/test$num/"

    # increasing the test number count for the next run
    echo "num=$num" > "/home/neo/monitor/Shell Scripts/Config/num.txt"
    echo "Test complete."

    # new lines for a clean log file
    echo ""
    echo ""
fi