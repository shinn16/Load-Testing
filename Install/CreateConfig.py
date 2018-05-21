
# @author Patrick Shinn
# @version 6/19/17

# getting input
ip = input("What is the IP of the machine you wish to monitor: ")
userName = input("What is the username you wish to use: ")
password = input("What is the password you wish to use: ")
dir = input("Give the path to Monitor.py excluding the file itself: ")
args = input("What arguments should be applied to Monitor.py: ")
analyze = input("What are the arguments for Analyze.py (--raw=True should probably be one): ")
machineType = input("What is the type of the machine? MySQL, Web, Driver: ")

# creating a configFile
configFile = machineType + "_Config.txt"
configFile = open("../Config/" + configFile, "w")

# Writing an config file for the LinuxRemoteMonitor shell script
print("Writing file...")
configFile.write("## Auto generated config file\n")
configFile.write("IP=" + ip + "\n")
configFile.write("USER_NAME=" + userName + "\n")
configFile.write("PASSWORD=" + password + "\n")
configFile.write("FOLDER=" + dir + "\n")
configFile.write("ARGS=\"" + args + "\"\n")
configFile.write("ANALYZE=\"" + analyze + "\"\n")
configFile.write("MACHINE=" + machineType)
configFile.close()
print("Done!")
