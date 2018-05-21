import psutil as util

i = 0
print("System Monitor Example\n"
      "--------------------------------------------------------------------------------------------------------")
while i < 5:
    # getting ram percentage used.
    ram = util.virtual_memory()  # gets ram
    swap = util.swap_memory()  # gets swap

    # filtering ram
    ram = str(ram).split("(")  # strips some stuff
    ram = ram[1]  # gets the meaningful stuff
    ram = ram.split(',')  # splits into indexable array
    ram = ram[1:3]
    for element in ram:
        element = element.strip(" ")
        print("ram_" + element, end="\t")

    # filtering swap
    swap = str(swap).strip("sswap(")
    swap = swap.split(",")
    for element in swap:
        if element.startswith(" used"):
            element = element.strip(" ")
            print("swap_" + element, end="\t")
        elif element.startswith(" percent"):
            element = element.strip(" ")
            print("swap_" + element, end="\t")

    # new line
    print()
    i += 1
