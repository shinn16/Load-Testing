import psutil as util
from optparse import OptionParser
import datetime

# @author Patrick Shinn
# @version 6/15/17


def main():
    # adding command line options
    parser = OptionParser()
    # parser.add_option("-f", "--configFile", help="Config file to be used at runtime.")
    parser.add_option("-c", "--configFile", help="Configuration file", default="None")
    parser.add_option("-r", "--runtime", help="Runtime in minutes", default=1)
    parser.add_option("-s", "--sampleTime", help="Time between each sample in seconds", default=2)
    parser.add_option("-t", "--type", help="The of machine to monitor, MySQL, Web, or Driver", default="TEST")
    parser.add_option("-o", "--output", help="Generate and output True, False", default=False)

    parsed_args = parser.parse_args()  # getting arguments
    args = parsed_args[0]  # refining arguments

    # getting arguments
    config_file = args.configFile
    sample = args.sampleTime
    output = args.output
    runs = args.runtime
    machine_type = args.type
    output_file = machine_type + "_output.csv"  # place holder for output file

    # checking to see if we need output
    if str(output).upper() == "TRUE":
        output = True
        output_file = open(output_file, "w")
    else:
        output = False

    # evaluating for what runs should be based on the time parameters.
    runs = int(runs) * 60 / int(sample)

    times_to_run = 0

    print("Config: " + config_file)
    print("Sample time: " + str(sample) + " second(s).")
    print("Runtime: " + str((runs * int(sample)) / 60) + " minute(s).")
    print("Writing to output file: " + str(output))
    print()
    print("Starting Monitor...")

    # used to keep track of network and disk usage

    # checking for configFile
    if config_file != "None":
        conf = open(config_file, "r")
        for line in conf:
            line = line.strip()
            line = line.split("=")
            if str(line[0]) == "sampleTime":
                sample = line[1]
            elif str(line[0]) == "runtime":
                runs = line[1]
            elif str(line[0] == "output"):
                if line[1].upper() == "TRUE":
                    output = True
                else:
                    output = False

    # used to compare data from disk_io and network_io
    base_data = [list(), list()]
    while times_to_run < int(runs):

        # getting time stamp
        current_time = datetime.datetime.now()
        current_time = str(current_time).split(" ")
        current_time = current_time[1]
        current_time = current_time.split(".")
        current_time = current_time[0]
        current_time = "Time=" + current_time

        # logging to output file if needed
        if output:
            output_file.write(current_time + "\t")
        else:
            print(current_time, end="\t")

        # monitors metrics
        cpu_stats(output, sample, output_file)
        ram_stats(output, output_file)
        network_io(output, base_data, output_file)
        disk_io(output, base_data, output_file)

        # new line
        if output:
            output_file.write("\n")
        else:
            print()
        times_to_run += 1


def cpu_stats(output, sample, output_file):
    """
    Monitors cpu data
    :param output: write to output file boolean
    :param sample: sample interval in seconds
    :param output_file: output file to be used if we need to write to one
    :return: none
    """
    cpu_count = util.cpu_count()  # number of cpus
    cpu_usage = util.cpu_percent(int(sample), True)  # gets the usage of each core and the time
    cpu_time = util.cpu_times(True)  # cpu times
    for cpu in range(cpu_count):
        # output cpu usage
        if output:
            output_file.write("CPU" + str(cpu) + " Usage=" + str(cpu_usage[cpu]) + "\t")
        else:
            print("CPU" + str(cpu) + " Usage=" + str(cpu_usage[cpu]), end="\t")

        # output cpu times
        times = cpu_time[cpu]  # get the current cpu's times
        times = str(times).split("(")  # getting rid of the cpu times label thing
        times = times[1]
        times = times.split(",")
        for items in times:  # iterates over the times and only gets system and idle
            items = items.strip(" ")
            if items.startswith("system"):  # gets system time
                if output:
                    output_file.write("CPU" + str(cpu) + "time_" + items + "\t")
                else:
                    print("CPU" + str(cpu) + "time_" + items, end="\t")
            elif items.startswith("idle"):  # gets idle time
                if output:
                    output_file.write("CPU" + str(cpu) + "time_" + items + "\t")
                else:
                    print("CPU" + str(cpu) + "time_" + items, end="\t")


def ram_stats(output, output_file):
    """
    Monitors ram data
    :param output: write to output file boolean
    :param output_file: output file to be used if we need to write to one
    :return: none
    """
    ram = util.virtual_memory()  # gets ram
    swap = util.swap_memory()  # gets swap

    # filtering ram
    ram = str(ram).split("(")  # strips some stuff
    ram = ram[1]  # gets the meaningful stuff
    ram = ram.split(',')  # splits into indexable array
    ram = ram[1:3]
    for element in ram:
        element = element.strip(" ")
        if output:
            output_file.write("ram_" + element + "\t")
        else:
            print("ram_" + element, end="\t")

    # filtering swap
    swap = str(swap).strip("sswap(")
    swap = swap.split(",")
    for element in swap:
        if element.startswith(" used"):
            element = element.strip(" ")
            if output:
                output_file.write("swap_" + element + "\t")
            else:
                print("swap_" + element, end="\t")
        elif element.startswith(" percent"):
            element = element.strip(" ")
            if output:
                output_file.write("swap_" + element + "\t")
            else:
                print("swap_" + element, end="\t")


def network_io(output, base_data, output_file):
    """
    Gets network io data
    :param output: write to output file boolean
    :param base_data: data used to compare data from last run
    :param output_file: output file to be used if we need to write to one
    :return: none
    """
    # getting the network usage
    network_usage = util.net_io_counters()
    # we now need to manipulate the string output
    network_usage = str(network_usage).split(',')
    network_usage[0] = network_usage[0].strip("snetio(")
    network_usage[len(network_usage) - 1] = network_usage[len(network_usage) - 1].rstrip(")")
    for info in range(len(network_usage)):
        network_usage[info] = network_usage[info].split("=")
        try:
            current_info = network_usage[info][1]
            usable_data = int(current_info) - int(base_data[0][info])
            base_data[0][info] = current_info
            if output:
                output_file.write(network_usage[info][0] + "=" + str(usable_data) + "\t")
            else:
                print(network_usage[info][0] + "=" + str(usable_data), end="\t")
        except IndexError:  # build the old data array
            base_data[0].append(network_usage[info][1])
            if output:
                output_file.write(network_usage[info][0] + "=0" + "\t")
            else:
                print(network_usage[info][0] + "=0", end="\t")


def disk_io(output, base_data, output_file):
    """
    Monitors disk io
    :param output: write to output file boolean
    :param base_data: data used to compare data from last run
    :param output_file: output file to be used if we need to write to one
    :return: none
    """
    disk_counter = util.disk_io_counters()  # getting counters
    disk_counter = str(disk_counter).strip("sdiskio(")  # cleaning counters
    disk_counter = disk_counter.split(",")
    disk_counter = disk_counter[0:4]
    for info in range(len(disk_counter)):  # working with the data
        disk_counter[info] = disk_counter[info].split("=")
        try:  # try to compare new dat to old data
            current_info = disk_counter[info][1]
            usable_data = int(current_info) - int(base_data[1][info])
            base_data[1][info] = current_info
            if output:
                output_file.write(disk_counter[info][0] + "=" + str(usable_data) + "\t")
            else:
                print(disk_counter[info][0] + "=" + str(usable_data), end="\t")
        except IndexError:  # build the old data array, we don't have one yet
            base_data[1].append(disk_counter[info][1])
            if output:
                output_file.write(disk_counter[info][0] + "=0" + "\t")
            else:
                print(disk_counter[info][0] + "=0", end="\t")

main()
