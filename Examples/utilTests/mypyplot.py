import matplotlib.pyplot as plt

'''
x = [3,4,5,6,7,8]
y = [5,2,6,8,7,4,9]
plt.plot(x, label="Line 1")
plt.plot(y, label="Line 2")
plt.title("Tester")
plt.ylabel("Y axis")
plt.xlabel("Xaxis")
plt.legend()
plt.show()
'''

file = open("/home/neo/Desktop/mypsutil/Output/2017-06-16 11:07:51.csv", "r")

firstRun = True

dataSets = list()

for line in file:
    line.strip()
    line = line.split("\t")
    if firstRun:
        for item in line:  # make a new list for each data header
            dataBlock = list()
            dataBlock.append(item)
            dataSets.append(dataBlock)
        firstRun = False
    else:
        for i in range(len(line)):
            print(line[i])
            list(dataSets[i]).append(line[i])
print(dataSets)
