import datetime

currentTime = datetime.datetime.now()
currentTime = str(currentTime).split(" ")
currentTime = currentTime[1]
currentTime = currentTime.split(".")
currentTime = currentTime[0]
print(currentTime)