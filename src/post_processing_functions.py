from src.classes import *
import numpy as np
from src import reading_functions as rf
from collections import Counter

def pixels_to_peaks(original, unet_output, threshold, left_offset):
    result = unet_output > threshold

    # TODO: Add some kind of pre-processing smoothing?

    for dye in range(result.shape[1]-1):
        # don't iterate over ladder
        current = result[:, dye]
        index_start = 0
        while index_start != len(current) - 1:
            # find next True
            while current[index_start] == False and index_start < len(current) - 1:
                index_start += 1
            index_end = index_start
            # find corresponding end True
            while current[index_end] == True and index_end < len(current) - 1:
                index_end += 1

            # TODO: add a check for amount of peaks/no peak?
            # more than 10 pixels is first requirement
            if index_end - index_start < 10:
                index_start = index_end
            else:
                # TODO: add a peak splitter of some kind?

                # find out which bins it contains
                # print(unet_output[index_start:index_end, dye])
                possible_alleles = allele_map[index_start+left_offset:index_end+left_offset, dye]
                # print(possible_alleles)
                print("Decision: ", Counter(possible_alleles).most_common(3))
                # some more magic should happen here
                index_start = index_end
    pass
#
#
# def find_closest_allele(max_index, dye_index):
#     # Have: location in array where a peak is
#     # Want: allele it belongs to
#     # Do I need the probabilities/window for the peak as well?
#     return allele_map[max_index, dye_index]

def peak_oriented_loss():
    pass

def peak_metric(unet_output, left_offset):
    peak_list = print_all_peaks("1A2")
    for key_locus in locus_dict:
        locus = locus_dict[key_locus]  # get locus class object
        alleles = locus.alleles
        for key_allele in alleles:
            allele = alleles[key_allele]
            start = -left_offset + round(10*(allele.mid-allele.left))
            stop = -left_offset + round(10*(allele.mid+allele.right))
            kansop = np.average(unet_output[start:stop,locus.index])
            if kansop > 0.5:
                print(key_locus, key_allele, kansop, (str(key_locus+"_"+key_allele) in peak_list))
    # go over all alleles
    # check probability of there being a peak
    # either do or don't call peak
    # I am afraid there will be too many positively identified bins
    pass


def print_all_peaks(mix_name):
    person_mix = rf.make_person_mixture(mix_name)
    peak_list = []
    # iterate through persons in mix
    for person in person_mix.persons:
        # iterate over their alleles
        for locus_allele in person.alleles:
            if locus_allele not in peak_list:
                peak_list.append(locus_allele)
    print(peak_list)
    return peak_list