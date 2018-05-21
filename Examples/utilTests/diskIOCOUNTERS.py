import psutil as util
import time

i = 0

baseData = [list(), list()]
print("System Monitor Example\n"
      "--------------------------------------------------------------------------------------------------------")
while i < 10:
    diskCounter = util.disk_io_counters()
    diskCounter = str(diskCounter).strip("sdiskio(")
    diskCounter = diskCounter.split(",")
    diskCounter = diskCounter[0:4]
    for info in range(len(diskCounter)):
        diskCounter[info] = diskCounter[info].split("=")
        try:
            currentInfo = diskCounter[info][1]
            usableData = int(currentInfo) - int(baseData[1][info])
            baseData[1][info] = currentInfo
            print(diskCounter[info][0] + "=" + str(usableData), end="\t")
        except IndexError:  # build the old data array
            baseData[1].append(diskCounter[info][1])
            print(diskCounter[info][0] + "=" + str(0), end="\t")
    print()
    time.sleep(2)
    # new line
    i += 1
