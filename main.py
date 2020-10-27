def read_func(filename):
    textfile = open(filename,"r")
    line1 = textfile.readline()
    line2 = textfile.readline()
    for i in range(20):
        line = textfile.readline()
        splitted = line.split("\t")
        print(len(splitted))
    return [line1,line2]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    line1,line2 = read_func('SizedTraceData.txt')
    print(line1.split(" "))
    print(line2.split(" "))