from optparse import OptionParser
import datetime

# @author Patrick Shinn
# @version 6/15/17

# setting up command line options
parser = OptionParser()
parser.add_option("-a", "--raw", help="Process a raw output file", default="False")
parser.add_option("-s", "--sampleTime", help="Time between samples in seconds", default=2)
parser.add_option("-t", "--type", help="Type of machine the data came from, MySQL, Web, or Driver")
parser.add_option("-c", "--compact", help="Compact data based on time in minutes. For example, if 1 were passed"
                                          "as the argument, then all of the data samples from a one minute time"
                                          "time span would be compacted and averaged into one data point. If you do not"
                                          "want to compact the data, put 0",
                  default=1)

# getting the args
args = parser.parse_args()
args = args[0]  # cleans the argument array
raw = args.raw
time = args.sampleTime
compact = int(args.compact)
machineType = args.type

print("Data collected in " + str(time) + " second(s) intervals")
print("Data blocks compacted into " + str(compact) + " minute blocks.")
print("Compacting data...")

if str(raw).upper() == "TRUE":
    raw = True
else:
    raw = False

# calculating compacting numbers
if compact == 0:
    compactNumber = 0
else:
    compactNumber = 60/int(time)*compact  # 60/time gets the data points per minute, multiply by the minutes to comp

# generating data file name by current time
preName = datetime.datetime.now()
preName = str(preName).split(" ")
preName[1] = preName[1].split(".")
preName = preName[0] + "_" + preName[1][0]

# adding path and extension to files
rawFile = "Output/" + machineType + "-" + preName + "-RAW.csv"
fileName = "Output/" + machineType + "-" + preName + ".csv"


# setting up files
fileToRead = machineType + "_output.csv"
dataFile = open(fileToRead, "r")  # read
rawDataFile = open(rawFile, "w")  # raw file copy
outFile = open(fileName, "w")  # compacted file
process = False

# if we are not processing raw output, just start processing
if not raw:
    process = True

# setting up to compact data
headerRow = list()
blocksProcessed = 0  # keeps track of how many blocks we have processed.
firstRun = True  # we use this to strip out the header info
dataList = list()  # storage space to save lists to before averaging
numberOfRuns = 0

for line in dataFile:
    rawDataFile.write(line)  # making a copy of raw data to preserve the data
    line = line.strip()
    dataPoint = list()  # clean list

    if not process:  # if we have to iterate past start, just do it
        if line.startswith("Starting"):  # go until we find the start, then begin processing
            process = True

    else:  # else, process the data
        numberOfRuns += 1  # keeps track of how many lines we have run over
        line = line.split("\t")  # split the line into and array

        for element in line:  # for every line, split it and get the values
            element = element.split("=")
            dataPoint.append(element[1])
            if firstRun:
                headerRow.append(element[0])

        if firstRun:  # extract the header row
            for header in headerRow:
                outFile.write(header + "\t")
            outFile.write("\n")
            firstRun = False

        # append the data to the dataList
        dataList.append(dataPoint)

        blocksProcessed += 1
        if compact != 0:  # only compact if we are told to
            timeStamp = True  # this will be used to stamp the compacted data
            if blocksProcessed == compactNumber:  # if we have processed enough blocks, average and compact
                outData = list()  # the final data to be written out
                for point in dataList:  # for every data point we have, average them
                    for data in range(len(point)):
                        if data != 0:  # skips the time stamp
                            try:
                                outData[data] += float(point[data])  # add the previous data points together
                            except IndexError:
                                outData.append(float(point[data]))  # there is no previous data, so just append.
                        else:  # if we are on the time stamp
                            if timeStamp:  # if this is the first run of this data compacting, keep the first time stamp
                                outData.append(point[data])
                                timeStamp = False  # we have already time stamped, no need to keep doing it.

                for data in range(len(outData)):
                    if data != 0:  # skip the time stamp so we don't average it
                        outData[data] = outData[data] / compactNumber  # after adding all the numbers, average them.
                    outFile.write(str(outData[data]) + "\t")
                outFile.write("\n")
                dataList.clear()
                blocksProcessed = 0  # reset blocks processed


if compact == 0:  # if we did not compact the data, we need to write the newly formatted csv out still
    for line in dataList:
        for element in line:
            outFile.write(str(element) + "\t")
        outFile.write("\n")
    print("Done!")

else:   # print out the compact stats
    print("Done! Compacted " + str(numberOfRuns) + " lines.")

# closing files
rawDataFile.close()
dataFile.close()
outFile.close()
