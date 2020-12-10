from src.classes import *
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
from skimage.segmentation import watershed


#NEEDS TO BE REVISED OR REPLACED
def create_input_list(sample: Sample, width: int):
    """Takes Sample, returns list of Inputs"""
    # width is 80 or 200
    sample_data = sample.data
    input_list = []
    for i in range(len(sample_data)-width):
        window = sample_data[i: i + width+1, :].copy()
        center_location = (i + width + 1) / 10
        for index in range(6):
            new_center = Center(center_location, Dyes().color_list[index])
            new_input = WrongInput(sample.name + "_" + str(i) + "_" + str(index), window, new_center, 0)
            input_list.append(new_input)
    return input_list


# should have approximately that shape, but need to decide what to do about other colours.
def create_input_from_sample(sample: Sample, width: int):
    sample_data = sample.data
    window_list = []
    for i in range(len(sample_data)-width):
        window = sample_data[i: i + width+1, :].copy()
        center_location = i + width + 1
        window_list.append(window)
    labels = labeler(sample)
    input_from_sample = TrainInput(sample, window_list, labels)
    return input_from_sample



def find_peak_locations(sample):
    one_array = sample.data[:,0]
    # peaks_indices, rest = find_peaks(one_array, width = 10, prominence = 80)
    # peak_bools = [True if i in peaks_indices else False for i in range(len(one_array))]
    # other interesting keywords: prominence (distance to baseline), wlen/width can give maximum too,
    # plateau size might be interesting on inverted image if it can handle noise
    # peak_bools = peak_local_max(one_array, min_distance = 100, indices = False)
    peak_bools = one_array > 100
    # also interesting: min_distance, num_peaks, chooses highest peaks if exceeded
    return one_array, peak_bools


def find_curves():
    pass


#####################PROBABLY WONT BE USED ANYMORE
def label_maker(person_mix, locus_dict):
    peaks = person_mix.create_peaks(locus_dict)
    label_list = [[], [], [], [], [], []]
    # cannot find precise index, since "size" of bins is accurate to 2 decimals, measurements to 1
    for peak in peaks:
        # should i also add approximate height in some way?
        x_val = round(peak.allele.mid*10)      # approximate index of peak
        dye_index = peak.allele.dye.plot_index - 1
        # intervals are all about 1 nucleotide wide at most, 0.8 at least
        label_list[dye_index].append(x_val)
        # now assumes bin size of 0.4 in both directions, actually wrong...
        for i in range(4):
            label_list[dye_index].append(x_val-i-1)
            label_list[dye_index].append(x_val+i+1)
    return label_list   # has indices of peaks per dye -> Why indices?

########NEEDS TO BE REVISED
def labeler(input_list, label_list):
    """Combines input list with label list for labeled entries"""
    for i in range(len(input_list)):
        if i + 41 in label_list[i % 6]:         # 41 steps from start is midpoint to be labeled
            input_list[i].label = 1             # always set to 1?
        else:
            input_list[i].label = 0
    return input_list
