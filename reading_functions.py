import numpy as np
import math as m
import matplotlib.pyplot as plt
import pandas as pd
from xml.dom import minidom
import xml.etree.ElementTree as ET
from csv import reader


def read_data(filename):
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


def read_data_old(filename):
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


def plot_data(data, titles, colors):
    """"Plots all single colors in lists"""
    counter = 0
    for i in range(len(titles)-1):
        for j in range(6):
            plt.figure()
            plt.plot(data[:, 6*i+j], label=str(colors[6*i+j]))
        plt.legend()
        plt.title(titles[counter])
        plt.show()
        counter += 1
    return None


def plot_6C(data, title, colors):
    """"Plots one 3x2 set of all 6 colors of one hid file"""
    fig = plt.figure()
    for i in range(6):
        plt.subplot(3, 2, i+1)
        plt.plot(data[:, i])
        plt.title(str(colors[i]))
    plt.show()
    return fig


def plot_compare(data_raw, data_sized, titles, colors):
    difference = len(data_raw)-len(data_sized)
    data_raw_short = data_raw[difference::, :]
    counter = 0
    for i in range(len(titles)-1):
        for j in range(6):
            plt.figure()
            plt.plot(data_raw_short[:, 6*i+j])
            plt.plot(data_sized[:, 6 * i + j])
            title = str(titles[i])+"_color_"+str(colors[6*i+j])
            plt.title(title)
            plt.show()
        counter += 1
    return None

def csv_read_actual(filename):
    """"Read csv file of actual alleles\
     combines with ???? for peak heights?"""
    # there may be more than one sample in one file
    pass


def csv_read_analyst(filename):
    """"Read csv file of identified alleles\
    returns list of alleles and corresponding peaks"""
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
        for i in range(2,12):
        # go over the 10 possible locations of peak identification
            if str(row[i]) == row[i]:
                # append value only if non-empty
                # empty entries are converted to (float-type) NaN's by pandas
                # so str(row[i]) == row[i] filters out empty entries
                allele_list.append(row[1]+"_"+row[i])
                # heights are 10 indices further than
                # their corresponding allele names
                height_list.append(row[i+10])
    return allele_lists, height_lists


def xml_read_bins(filename):
    """Read xml file for bins of each allele, \
    returns dictionary of horizontal values"""
    thetreefile = ET.parse(filename)
    root = thetreefile.getroot()
    # create a dictionary per color
    allele_dict = {}
    dye_dict = {}
    for locus in root[5]: # root[5] is the loci
        # get the name of the marker
        current_marker = locus.find('MarkerTitle').text
        # make dict of which locus belongs to which colour
        dye = locus.find('DyeIndex').text

        for allele in locus.findall('Allele'):
            # get the name of the allele (number or X/Y)
            allele_label = allele.get('Label')
            # combine marker+allele into key
            keyname = str(current_marker)+"_"+str(allele_label)
            # store the horizontal location as value
            valuename = str(allele.get('Size'))
            # still not sure about difference between Size and DefSize
            allele_dict[keyname] = valuename
            dye_dict[keyname] = int(dye)
    return allele_dict, dye_dict

def plot_actual(alleles, heights, allele_dict, dye_dict):
    plt.figure()
    for i in range(len(alleles)):
        # use dye_dict to plot correct color
        plt.subplot(6,1,dye_dict[alleles[i]])
        print(dye_dict[alleles[i]])
        plt.plot([allele_dict[str(alleles[i])]],[heights[i]],"*")
    plt.show()
    pass