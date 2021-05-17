from src.classes import *
import numpy as np

# def pixels_to_peaks(original, unet_output, threshold, left_offset):
#     result = unet_output.squeeze() > threshold
#
#     # TODO: Add some kind of pre-processing smoothing?
#
#     for dye in range(result.shape[1]):
#         current = result[:, dye]
#         index_start = 0
#         while index_start != len(current) - 1:
#             # find next True
#             while current[index_start] == False and index_start < len(current) - 1:
#                 index_start += 1
#             index_end = index_start
#             # find corresponding end True
#             while current[index_end] == True and index_end < len(current) - 1:
#                 index_end += 1
#
#             # TODO: add a check for amount of peaks/no peak?
#             # more than 10 pixels is first requirement
#             if index_start == index_end:
#                 pass
#             else:
#
#                 # TODO: add a peak splitter of some kind?
#
#                 # find index of max value (top of peak)
#                 top_of_peak = left_offset + index_start + np.argmax(original[index_start:index_end])
#                 # find out which bin it's in
#                 allele = find_closest_allele(top_of_peak, dye)
#                 print(allele)
#                 # some more magic should happen here
#                 index_start = index_end
#     pass
#
#
# def find_closest_allele(max_index, dye_index):
#     # Have: location in array where a peak is
#     # Want: allele it belongs to
#     # Do I need the probabilities/window for the peak as well?
#     return allele_map[max_index, dye_index]

def peak_oriented_loss():
    pass

def peak_metric(unet_output, threshold, left_offset):
    for key_locus in locus_dict:
        locus = locus_dict[key_locus]  # get locus class object
        alleles = locus.alleles
        for key_allele in alleles:
            allele = alleles[key_allele]
            start = -left_offset + round(10*(allele.mid-allele.left))
            stop = -left_offset + round(10*(allele.mid+allele.right))
            kansop = np.average(unet_output[start:stop,locus.index])
            if kansop > 0.9:
                print(key_locus, key_allele, kansop)
    # go over all alleles
    # check probability of there being a peak
    # either do or don't call peak
    # I am afraid there will be too many positively identified bins
    pass