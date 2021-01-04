from src.classes import *


#NEEDS TO BE REVISED OR REPLACED
def create_input_list(sample: Sample, width: int):
    """Takes Sample, returns list of Inputs"""
    # width is 160 or 200
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
    """For one electropherogram, creates all input (node) images and their labels."""
    sample_data = sample.data
    window_list = []
    for i in range(len(sample_data)-width):
        window = sample_data[i: i + width+1, :].copy()
        center_location = i + width + 1
        window_list.append(window)
    label_list = labeler(sample)
    input_from_sample = TrainInput(sample, window_list, label_list)
    return input_from_sample


def bin_indices_maker(person_mix):
    """Makes array of indices where a peak is expected based on the bins."""
    peaks = person_mix.create_peaks()
    bin_indices = [[], [], [], [], [], []]
    # cannot find precise index, since "size" of bins is accurate to 2 decimals, measurements to 1
    for peak in peaks:
        left_index = round((peak.allele.mid - peak.allele.left)*10)
        right_index = round((peak.allele.mid + peak.allele.right)*10)
        dye_index = peak.allele.dye.plot_index - 1
        # intervals are all about 1 nucleotide wide at most, 0.8 at least
        bin_indices[dye_index] += list(np.arange(left_index, right_index))
    return bin_indices   # has indices of left to right side of each bin


def find_peaks_in_bins(sample: Sample, list_of_bins: list):
    """Makes array of True/False of same size as data. True if a peak should theoretically be visible\
    based on the composition and the bin locations, False otherwise."""
    only_blue = list_of_bins[0]
    blue_sample = sample.data[:,0]
    indices = [True if blue_sample[ind] > 80 and ind in only_blue else False for ind in range(len(blue_sample))]
    return np.array(indices)


def bin_finder(person_mix):
    peaks = person_mix.create_peaks()
    bin_edges = [[], [], [], [], [], []]
    # cannot find precise index, since "size" of bins is accurate to 2 decimals, measurements to 1
    for peak in peaks:
        # maybe always round left down and right up to enlarge interval a little?
        left_index = round((peak.allele.mid - peak.allele.left)*10)
        right_index = round((peak.allele.mid + peak.allele.right)*10)
        dye_index = peak.allele.dye.plot_index - 1
        # intervals are all about 1 nucleotide wide at most, 0.8 at least
        bin_edges[dye_index].append((left_index, right_index))
    return bin_edges   # has indices of left to right side of each bin


def find_peaks_flowing_out_of_bins(sample: Sample, list_of_bins: list):
    """Makes array of same size as data with True/False values if peak should be visible.
    Uses maximum within bin and follows whatever part of peak is visible to entire peak."""
    blue_bins = list_of_bins[0]
    blue_sample = sample.data[:, 0]
    bin_bool = [False]*len(blue_sample)
    for left, right in blue_bins:
        max_index = left + np.argmax(blue_sample[left:right+1])
        if blue_sample[max_index - 1] > blue_sample[max_index]:
            while blue_sample[max_index - 1] - blue_sample[max_index] > 1e-10:
                max_index -= 1
        elif blue_sample[max_index + 1] > blue_sample[max_index]:
            while blue_sample[max_index + 1] - blue_sample[max_index] > 1e-10:
                max_index += 1
        bin_bool[max_index] = True
        left_end = max_index
        right_end = max_index
        while blue_sample[left_end] - blue_sample[left_end-1] > 0:
            left_end -= 1
            bin_bool[left_end] = True
        while blue_sample[right_end] - blue_sample[right_end+1] > 0:
            right_end += 1
            bin_bool[right_end] = True
    return np.array(bin_bool)


