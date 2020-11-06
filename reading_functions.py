import numpy as np
import pandas as pd
import xml.etree.ElementTree as et


def txt_read_data(filename):
    """ Function to read data files\
    Returns a list of sample names, colors, \
    and the data itself as matrix."""
    textfile = open(filename, "r")
    texts = textfile.read()
    texts = texts.split("\n")
    # lines 1 and 2 are not interesting
    titles = texts[2].split('\t')                       # get titles of files
    titles = [item for item in titles if item != '']    # remove empty entries after splitting
    colors = texts[3].split('\t')                       # get names of colors
    data = np.zeros((len(texts[4:]), len(colors)))
    counter = 0
    for elt in texts[4:]:
        new = np.array(elt.split('\t'))
        new[new == ''] = 0
        data[counter, :] = new
        counter += 1
    return titles, colors, data


def txt_read_data_old(filename):
    """ Outdated: Function to read data files using readline"""
    textfile = open(filename, "r")
    textfile.readline()             # first two lines are not important
    textfile.readline()
    names = textfile.readline()     # names are separated by multiple tabs
    names = names.split("\t")
    names[:] = [item for item in names if item != '']   # remove empty entries (between two \t's)
    colors = textfile.readline()
    colors = colors.split("\t")
    colors[:] = [item for item in colors if item != '']
    data = []           # fill with data
    for i in range(5000):
        line = textfile.readline()
        splitted = line.split("\t")
        splitted[:] = [int(item) for item in splitted if (item != '' and item != '\n')]
        data.append(np.array(splitted))
    data = np.array(data)
    return names, colors, data


def xml_read_bins(filename):
    """Read xml file for bins of each allele, \
    returns dictionary of horizontal values"""
    thetreefile = et.parse(filename)
    root = thetreefile.getroot()
    # create a dictionary per color
    allele_dict = {}
    empty_dict = {}
    dye_dict = {}
    for locus in root[5]:  # root[5] is the loci
        # get the name of the marker
        current_marker = locus.find('MarkerTitle').text
        # make dict of which locus belongs to which colour
        temp_dict = {1: 'FL-6C', 2: 'JOE-6C', 3: 'TMR-6C', 4: 'CXR-6C', 6: 'TOM-6C'}
        dye = locus.find('DyeIndex').text
        dye_dict[current_marker] = temp_dict[int(dye)]
        allele_dict[current_marker] = {}
        empty_dict[current_marker] = {}
        for allele in locus.findall('Allele'):
            # get the name of the allele (number or X/Y)
            allele_label = allele.get('Label')
            # combine marker+allele into key
            # keyname = str(current_marker)+"_"+str(allele_label)
            # store the horizontal location as value
            valuename = float(allele.get('Size'))
            # still not sure about difference between Size and DefSize
            allele_dict[current_marker][allele_label] = valuename
            empty_dict[current_marker][allele_label] = 0
    return allele_dict, dye_dict, empty_dict


def csv_read_actual(filename, goalname, allele_peaks):
    """Read csv file of actual alleles\
     combines with info in word file for peak heights?"""
    # there may be more than one sample in one file
    # goalname can be 1A2 for example
    donor_peaks = pd.read_csv(filename, dtype = str, delimiter = ";")
    donor_set, mixture_type, number_of_donors = goalname
    # check if names match, otherwise donorset is different and output makes no sense
    if filename[-5] != donor_set:
        print("Filename "+filename+" does not match "+donor_set)
        return None
    ############################################################################3
    #   All this could be done anywhere, just don't have a location for it
    #   A: 	300:150	300:150:150	300:150:150:150	300:150:150:150:150
    #   B: 	300:30	300:30:30	300:30:30:30	300:30:30:30:30
    #   C: 	150:150	150:150:60	150:150:60:60	150:150:60:60:60
    #   D:	150:30	150:30:60	150:30:60:30	150:30:60:30:30
    #   E:	600:30	600:30:60	600:30:60:30	600:30:60:30:30
    # relative contributions
    #   A:  2:1     2:1:1       2:1:1:1         2:1:1:1:1
    #      2/3:1/3  .5:.25:.25  .4:.2:.2:.2     2/7:1/7:1/7
    #   B: 10:1     10:1:1      10:1:1:1        10:1:1:1:1
    #      10/11:1/11
    picograms = np.array([[300, 150, 150, 150, 150],
                          [300, 30,  30,  30,  30],
                          [150, 150, 60,  60,  60],
                          [150, 30,  60,  30,  30],
                          [600, 30,  60,  30,  30]])
    total_picograms = np.zeros((5,4))
    for i in range(5):
        row = picograms[i]
        for j in range(4):
            total_picograms[i,j] = sum(row[:j+2])
    #########################################################################3
    # mixture_type decides which row of matrix to use
    # number_of_donors decides which column in totals
    letter_to_number = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    current = letter_to_number[mixture_type]
    parts = picograms[current]
    total = total_picograms[current,int(number_of_donors)-2]
    # initialize column/donor
    donor = 0
    # intialize comparison variable
    sample = donor_peaks["SampleName"][0]
    for index, row in donor_peaks.iterrows():
        if row[0] != sample:
            donor += 1
        if donor >= int(number_of_donors):
            # break if amount of donors is reached
            break
        sample = row[0]
        allele_peaks[row[1]][row[2]] += parts[donor]/total  # Allele 1
        allele_peaks[row[1]][row[3]] += parts[donor]/total  # Allele 2
    return allele_peaks


def csv_read_analyst(filename):
    """"Read csv file of identified alleles\
    returns list of alleles and corresponding peaks
    allele list is nested list per sample"""
    # I can use output of xml_read_bins to find colors of alleles
    # there may be more than one sample in one file
    results = pd.read_csv(filename)
    name = results['Sample Name'][0]    # to start iteration
    allele_lists = []                   # initialize big lists
    height_lists = []
    allele_list = []                    # initialize small lists
    height_list = []
    for index, row in results.iterrows():
        # iterate over all rows, because each row contains
        # the peaks for one locus
        if name != row[0]:                      # then start new sample
            allele_lists.append(allele_list)    # store current sample data
            height_lists.append(height_list)
            allele_list = []                    # empty lists
            height_list = []
        name = row[0]                           # then set name to current sample name
        for i in range(2, 12):
            # go over the 10 possible locations of peak identification
            if str(row[i]) == row[i]:
                # append value only if non-empty
                # empty entries are converted to (float-type) NaN's by pandas
                # so str(row[i]) == row[i] filters out empty entries
                allele_list.append(row[1]+"_"+row[i])
                # heights are 10 indices further than
                # their corresponding allele names
                height_list.append(row[i+10])
    allele_lists.append(allele_list)
    height_lists.append(height_list)
    return allele_lists, height_lists
