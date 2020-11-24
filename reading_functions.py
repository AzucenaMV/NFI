import pandas as pd
import xml.etree.ElementTree as eT
from classes import *


def txt_read_data(filename: str):
    """ Function to read data files\
    Returns a list of sample names, colors, \
    and the data itself as matrix."""
    textfile = open(filename, "r")  # open text file
    texts = textfile.read()         # read entire content
    texts = texts.split("\n")       # split into lines
    # lines 1 and 2 are not interesting
    titles = texts[2].split('\t')                       # get titles of files
    titles = [item for item in titles if item != '']    # remove empty entries after splitting
    colors = texts[3].split('\t')                       # only needed for width of lines
    data = np.zeros((len(texts[4:]), len(colors)))
    counter = 0         # counter is needed for line number
    for elt in texts[4:]:
        new = np.array(elt.split('\t'))     # split into words
        new[new == ''] = 0                  # if empty, make zero
        data[counter, :] = new              # store into data array
        counter += 1
    # now pour contents into separate sample dataclasses
    sample_list = []
    for i in range(len(titles)):
        new_sample = Sample(titles[i].split('_')[0], data[:, 6*i:6*i+6])
        sample_list.append(new_sample)
    return sample_list


def xml_read_bins():
    """Read xml file for bins of each allele, \
    returns dictionary of horizontal values"""

    thetreefile = eT.parse("PPF6C_SPOOR.xml")
    root = thetreefile.getroot()
    locus_dict = {}
    # root[5] is the loci
    for locus in root[5]:
        locus_name = locus.find('MarkerTitle').text
        # to translate the numbers in xml file to colors
        temp_dict = {1: BLUE, 2: GREEN, 3: YELLOW, 4: RED, 5: LADDER, 6: PURPLE}
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
            new_allele = Allele(allele_name, mid, left, right)
            # add to alleles dict of locus
            new_locus.alleles[allele_name] = new_allele
        # add created locus to locus dict
        locus_dict[locus_name] = new_locus
    return locus_dict


def csv_read_persons(donor_set):
    """reads all profiles from given donorset (1,2,3,4,5,6)"""
    filename = 'donor_profiles/Refs_dataset' + str(donor_set) + '.csv'
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
        allele1 = locus + "_" + row[2]
        allele2 = locus + "_" + row[3]
        alleles.append(allele1)
        alleles.append(allele2)
    return person_list


def person_contributions(person_list, number_of_donors: int, mixture_type: str):
    letter_to_number = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    mixture_row = letter_to_number[mixture_type]    # type of mixture determines the row
    person_dict = {}
    persons = []
    parts = PICOGRAMS[mixture_row]
    total = TOTAL_PICOGRAMS[mixture_row, number_of_donors - 2]
    for i in range(number_of_donors):
        frac = parts[i]/total/2     # divide by 2 because 2 alleles per locus
        person_dict[person_list[i].name] = frac   # should I already divide by 2 here?
        persons.append(person_list[i])
    return person_dict, persons


def make_person_mixture(mixture_name, locus_dict):
    donor_set, mixture_type, donor_amount = mixture_name
    # just a small thing, but always need to convert this one to int, \
    # better to do in function or outside of function and specify it needs
    # to be an int in the function?
    donor_amount = int(donor_amount)
    person_list = csv_read_persons(donor_set)
    person_fracs, persons = person_contributions(person_list, donor_amount, mixture_type)
    person_mix = PersonMixture(mixture_name, persons, person_fracs)
    peaks = person_mix.create_peaks(locus_dict)
    return peaks


def csv_read_analyst(sample_name, locus_dict):
    """Read csv file of identified alleles\
    returns list of corresponding peaks"""
    results = pd.read_csv("analysts_data_filtered/"+str(sample_name)+"_New.csv")
    name = results['Sample Name'][0]    # to start iteration
    sample_name, replicate = name.split('.') # is it okay to add a useless statement to get rid of a pycharm warning?
    mixture_list = []                   # initialize big lists
    peak_list = []                      # initialize small lists
    for index, row in results.iterrows():
        # iterate over all rows, because each row contains
        # the peaks for one allele
        if name != row[0]:                      # then start new sample
            sample_name, replicate = name.split('.')
            mixture_list.append(AnalystMixture(sample_name, replicate, peak_list))    # store current sample data
            peak_list = []                      # empty list
        name = row[0]                           # then set name to current sample name
        for i in range(2, 12):
            # go over the 10 possible locations of peak identification
            if str(row[i]) == row[i]:
                # append value only if non-empty
                # empty entries are converted to (float-type) NaN's by pandas
                # so str(row[i]) == row[i] filters out empty entries
                locus = locus_dict[row[1]]
                allele = locus.alleles[row[i]]
                x_value = allele.mid
                height = row[i+10]  # heights are 10 indices further than
                dye = locus.dye     # their corresponding allele names
                new_peak = Peak(locus.name+"_"+allele.name, x_value, height, dye)
                peak_list.append(new_peak)
    mixture_list.append(AnalystMixture(name, replicate, peak_list))
    return mixture_list
