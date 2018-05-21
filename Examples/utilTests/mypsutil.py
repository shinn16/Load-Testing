import psutil as util

i = 0
cpuCount = util.cpu_count()

print("System Monitor Example\n"
      "--------------------------------------------------------------------------------------------------------")
while i < 5:
    cpuUsage = util.cpu_percent(2, True)
    for cpu in range(cpuCount):
        print("CPU" + str(cpu) + " Usage: " + str(cpuUsage[cpu]) + "%", end="\t")

    # getting ram percentage used.
    ram = util.virtual_memory()  # gets ram
    ram = str(ram).split(',')  # splits into indexable array
    ram = ram[2]  # gets the percent used
    print("Ram used: " + ram + "%", end="\t")

    # cpu times
    cpuMetrics = util.cpu_times(True)
    print(cpuMetrics)

    # getting number of processes
    processes = util.pids()  # gets a list of pids
    numberOfProcesses = len(processes)
    print("Processes: " + str(numberOfProcesses), end="\t")

    # getting the network usage
    networkUsage = util.net_io_counters()
    # we now need to manipulate the string output
    networkUsage = str(networkUsage).split(',')
    networkUsage[0] = networkUsage[0].strip("snetio(")
    networkUsage[len(networkUsage) - 1] = networkUsage[len(networkUsage) - 1].rstrip(")")
    print("Network Info: ", end="")
    for info in networkUsage:
        print(info, end="\t")

    # new line
    print()
    i += 1


print("\n"
      "Process info\n"
      "--------------------------------------------------------------------------------------------------------")
i = 0
for proc in util.process_iter():  # iterates of all system processes in order of pid.
    try:
        # gets the info with the attached attribute name, not in the order of the attr array.
        pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'cpu_times'])
    except util.NoSuchProcess:
        pass
    else:
        print(pinfo)

    i += 1
    if i == 5:  # this is just a test and we are not looking for a particular process, so just print the first 5
        break

print("\n"
      "Getting particular process with its info, in this case python3.6, this name may vary by OS. Works on Linux.\n"
      "--------------------------------------------------------------------------------------------------------")
procName = "python3.6"
for proc in util.process_iter():
    if proc.name() == procName:
        try:
            # gets the info with the attached attribute name, not in the order of the attr array.
            pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'cpu_times'])
        except util.NoSuchProcess:
            pass
        else:
            print(pinfo)
