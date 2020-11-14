import pandas as pd
import xml.etree.ElementTree as eT
from GLOBALS import *


def txt_read_data(filename: str):
    """ Function to read data files\
    Returns a list of sample names, colors, \
    and the data itself as matrix."""
    textfile = open(filename, "r")
    texts = textfile.read()
    texts = texts.split("\n")
    # lines 1 and 2 are not interesting
    titles = texts[2].split('\t')                       # get titles of files
    titles = [item for item in titles if item != '']    # remove empty entries after splitting
    colors = texts[3].split('\t')                       # only needed for width of lines
    data = np.zeros((len(texts[4:]), len(colors)))
    counter = 0
    for elt in texts[4:]:
        new = np.array(elt.split('\t'))
        new[new == ''] = 0
        data[counter, :] = new
        counter += 1

    sample_list = []
    for i in range(len(titles)):
        new_sample = Sample(titles[i].split('_')[0], data[:, 6*i:6*i+6])
        sample_list.append(new_sample)
    return sample_list


# def xml_read_bins(filename: str) -> Locus:
def xml_read_bins(filename: str):
    """Read xml file for bins of each allele, \
    returns dictionary of horizontal values"""

    # Only want to define each color once, maybe in GLOBALS.py?
    blue = Dye('FL-6C', 'b', 1)
    green = Dye('JOE-6C', 'g', 2)
    yellow = Dye('TMR-6C', 'y', 3)
    red = Dye('CXR-6C', 'r', 4)
    purple = Dye('TOM-6C', 'm', 5)
    ladder = Dye('WEN-6C', 'k', 6)

    thetreefile = eT.parse(filename)
    root = thetreefile.getroot()
    locus_dict = {}
    # root[5] is the loci
    for locus in root[5]:
        locus_name = locus.find('MarkerTitle').text
        # to translate the numbers in xml file to colors
        temp_dict = {1: blue, 2: green, 3: yellow, 4: red, 5: ladder, 6: purple}
        dye = int(locus.find('DyeIndex').text)
        lower = float(locus.find('LowerBoundary').text)
        upper = float(locus.find('UpperBoundary').text)
        # store info so far in Locus dataclass
        new_locus = Locus({}, locus_name, temp_dict[dye], lower, upper)
        # add all alleles to locus
        for allele in locus.findall('Allele'):
            allele_name = allele.get('Label')
            mid = float(allele.get('Size'))
            left = float(allele.get('Left_Binning'))
            right = float(allele.get('Right_Binning'))
            # store in Allele dataclass
            new_allele = Allele(allele_name, mid, left, right, locus_name, 0)
            # add to alleles dict of locus
            new_locus.alleles[allele_name] = new_allele
        # add created locus to locus dict
        locus_dict[locus_name] = new_locus
    return locus_dict


def csv_read_persons(donorset, locus_dict):
    """reads all profiles from donorset"""
    filename = 'donor_profiles/Refs_dataset' + str(donorset) + '.csv'
    donor_peaks = pd.read_csv(filename, dtype=str, delimiter=";")
    person_list = []
    alleles = []
    person_name = donor_peaks['SampleName'][0]
    for index, row in donor_peaks.iterrows():
        if row[0] != person_name:
            # we have arrived at a new person
            # store up to now in Person, start new
            person_list.append(Person(person_name, alleles))
            alleles = []
        person_name = row[0]
        locus = row[1]
        allele1 = locus_dict[locus].alleles[row[2]]
        allele2 = locus_dict[locus].alleles[row[3]]
        alleles.append(allele1)
        alleles.append(allele2)
    return person_list


def make_mixture(personlist, mixturename: str, locus_dict):
    """ Uses Persons and mixturename to combine into expected relative peakheights"""
    # mixturename can be 1A2 for example
    # expected string of length 3, so unpack each character
    donor_set, mixture_type, number_of_donors = mixturename
    number_of_donors = int(number_of_donors)
    # mixture_type decides which row of picogram matrix to use
    # number_of_donors decides which column in picogram total matrix
    # ############## COULD DO THIS IN SEPARATE FUNCTION #####################
    letter_to_number = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    mixtype = letter_to_number[mixture_type]
    parts = picograms[mixtype]
    total = total_picograms[mixtype, number_of_donors-2]

    for i in range(number_of_donors):
        allele_list = personlist[i].alleles
        for allele in allele_list:
            relative = parts[i]/total/2
            locus_dict[allele.marker].alleles[allele.name].height += relative

    allele_list = []
    height_list = []
    for key in locus_dict:
        allele_dict = locus_dict[key].alleles
        for key2 in allele_dict:
            value2 = allele_dict[key2]
            if value2.height != 0:
                allele_list.append(value2)
                height_list.append(value2.height)

    new_mixture = Mixture(mixturename, allele_list, height_list)
    return new_mixture


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
