def read_func(filename):
    textfile = open(filename,"r")
    names = textfile.readline()
    names = textfile.readline()
    names = textfile.readline()

    for i in range(20):
        line = textfile.readline()
        splitted = line.split("\t")
        splitted[:] = [item for item in splitted if item != '']
        print(len(splitted))
    return None

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_func('SizedTraceData.txt')
