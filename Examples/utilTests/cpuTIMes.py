import psutil as util

i = 0
cpuCount = util.cpu_count()

print("System Monitor Example\n"
      "--------------------------------------------------------------------------------------------------------")
while i < 10:

    # cpu times
    cpuTime = util.cpu_times(True)
    for times in cpuTime:
        times = str(times).split("(")  # getting rid of the cpu times label thing
        times = times[1]
        times = times.split(",")
        for element in times:
            element = element.strip(" ")
            if element.startswith("system"):
                print("time_" + element, end="\t")
            elif element.startswith("idle"):
                print("time_" + element, end="\t")
        print()
    print()
    i += 1
