import pandas as pd
import xml.etree.ElementTree as eT
from src.classes import *


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
    counter = 0                                         # counter is needed for line number
    for elt in texts[4:]:
        new = np.array(elt.split('\t'))     # split into words
        new[new == ''] = 0                  # if empty string, make zero
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
    returns dictionary of information"""
    tree_file = eT.parse("data/PPF6C_SPOOR.xml")
    root = tree_file.getroot()
    locus_dict = {}
    # root[5] is the node with loci, rest is panel info
    for locus in root[5]:
        locus_name = locus.find('MarkerTitle').text
        # to translate the numbers in xml file to dyes
        temp_dict = {1: Dyes.BLUE, 2: Dyes.GREEN, 3: Dyes.YELLOW, 4: Dyes.RED, 5: Dyes.LADDER, 6: Dyes.PURPLE}
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
    """reads all profiles from given donor set (1,2,3,4,5 or 6)"""
    filename = 'data/donor_profiles/Refs_dataset' + str(donor_set) + '.csv'
    donor_peaks = pd.read_csv(filename, dtype=str, delimiter=";")
    person_list = []                            # initialize lists
    alleles = []
    person_name = donor_peaks['SampleName'][0]  # get first donor name
    for index, row in donor_peaks.iterrows():   # iterate over all alleles
        if row[0] != person_name:               # we have arrived at a new person
            # store up to now in Person dataclass, start new list
            person_list.append(Person(person_name, alleles))
            alleles = []
        person_name = row[0]                    # first entry is person name
        locus = row[1]                          # second entry is locus name
        allele1 = locus + "_" + row[2]          # third entry is first allele
        allele2 = locus + "_" + row[3]          # fourth entry is second allele
        alleles.append(allele1)
        alleles.append(allele2)
    return person_list


def person_contributions(person_list, number_of_donors: int, mixture_type: str):
    """Calculates relative contributions of each person based on mixture type"""
    # Temporary dict to translate letter to row
    letter_to_number = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    mixture_row = letter_to_number[mixture_type]    # type of mixture determines the row
    person_dict = {}                                # initialize list and dict
    persons = []
    parts = PICOGRAMS[mixture_row]                  # global variables for contributions
    total = TOTAL_PICOGRAMS[mixture_row, number_of_donors - 2]
    for i in range(number_of_donors):
        frac = parts[i]/total/2                     # divide by 2 because 2 alleles per locus
        person_dict[person_list[i].name] = frac     # add fraction to person
        persons.append(person_list[i])
    return person_dict, persons


def make_person_mixture(mixture_name, locus_dict):
    """Uses person_contributions and csv_read_persons to create expected peaks in person mixture"""
    donor_set, mixture_type, donor_amount = mixture_name        # can be "1A2" for example
    donor_amount = int(donor_amount)
    person_list = csv_read_persons(donor_set)
    person_fracs, persons = person_contributions(person_list, donor_amount, mixture_type)
    person_mix = PersonMixture(mixture_name, persons, person_fracs)
    return person_mix


def csv_read_analyst(sample_name, locus_dict):
    """Read csv file of analyst's identified alleles returns list of corresponding peaks"""
    results = pd.read_csv("data/analysts_data_filtered/"+str(sample_name)+"_New.csv")
    name = results['Sample Name'][0]    # to start iteration
    sample_name, replicate = name.split('.')
    mixture_list = []                   # initialize big lists
    peak_list = []                      # initialize small lists
    for index, row in results.iterrows():
        # iterate over all rows, because each row contains the peaks for one allele
        if name != row[0]:                      # then start new sample
            sample_name, replicate = name.split('.')
            mixture_list.append(AnalystMixture(sample_name, replicate, peak_list))
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
                x_value = allele.mid    # location on x_axis
                height = row[i+10]      # heights are 10 indices further than
                dye = locus.dye         # their corresponding allele names
                new_peak = Peak(locus.name+"_"+allele.name, x_value, height, dye)
                peak_list.append(new_peak)
    mixture_list.append(AnalystMixture(name, replicate, peak_list))
    return mixture_list
