import psutil as util
import time

i = 0
cpuCount = util.cpu_count()

print("System Monitor Example\n"
      "--------------------------------------------------------------------------------------------------------")
baseData = [list(), list()]
while i < 10:

    # getting the network usage
    networkUsage = util.net_io_counters()
    # we now need to manipulate the string output
    networkUsage = str(networkUsage).split(',')
    networkUsage[0] = networkUsage[0].strip("snetio(")
    networkUsage[len(networkUsage) - 1] = networkUsage[len(networkUsage) - 1].rstrip(")")
    for info in range(len(networkUsage)):
        networkUsage[info] = networkUsage[info].split("=")
        try:
            currentInfo = networkUsage[info][1]
            usableData = int(currentInfo) - int(baseData[0][info])
            baseData[0][info] = currentInfo
            print(networkUsage[info][0] + "=" + str(usableData), end="\t")
        except IndexError:  # build the old data array
            baseData[0].append(networkUsage[info][1])
            print(networkUsage[info][0] + "=" + str(0), end="\t")
    time.sleep(2)

    # new line
    print()
    i += 1
