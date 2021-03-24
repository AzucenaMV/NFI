from src.classes import *
import numpy as np
from src import reading_functions as rf

# should have approximately that shape, but need to decide what to do about other colours.
def create_input_from_sample(sample: Sample, width: int, person_mix, number_of_dyes):
    """For one electropherogram, creates all input (node) images and their labels."""
    # width is amount of steps in each direction, either 80 or 100
    sample_data = sample.data
    window_list = []
    # apparently, this works?
    labels = find_peaks_flowing_out_of_bins(sample, bin_lefts_rights(person_mix))
    label_list = []
    for i in range(len(sample_data) - 2 * width):
        window = sample_data[i: i + 2 * width + 1, :number_of_dyes].copy()
        center_location = i + width + 1
        window_list.append(window)
        label = labels[:number_of_dyes, center_location]
        label_list.append(label)
    input_from_sample = TrainInput(sample, np.array(window_list), np.array(label_list))
    return input_from_sample


def input_from_multiple_samples(samplelist: List[Sample], width: int, cutoff):
    """For one electropherogram, creates all input (node) images and their labels."""
    all_data = []
    all_labels = []
    for sample in samplelist:
        if len(sample.name) == 3:
            all_data.append(sample.data[:cutoff, :width])
            person_mix = rf.make_person_mixture(sample.name)
            labels = find_peaks_flowing_out_of_bins(sample, bin_lefts_rights(person_mix))
            all_labels.append(labels[:cutoff, :width])
    input_from_samples = NewTrainInput(np.array(all_data), np.array(all_labels))
    return input_from_samples


def bin_all_indices(person_mix):
    """Makes array of indices where a peak is expected based on the bins."""
    peaks = person_mix.create_peaks()
    bin_indices = [[], [], [], [], [], []]
    # cannot find precise index, since "size" of bins is accurate to 2 decimals, measurements to 1
    for peak in peaks:
        left_index = round((peak.allele.mid - peak.allele.left) * 10)
        right_index = round((peak.allele.mid + peak.allele.right) * 10)
        dye_index = peak.allele.dye.plot_index - 1
        # intervals are all about 1 nucleotide wide at most, 0.8 at least
        bin_indices[dye_index] += list(np.arange(left_index, right_index))
    return bin_indices  # has indices of left to right side of each bin


def bin_lefts_rights(person_mix):
    """Makes list of left and right sides of allelebins when expected"""
    peaks = person_mix.create_peaks()
    bin_edges = [[], [], [], [], [], []]
    # cannot find precise index, since "size" of bins is accurate to 2 decimals, measurements to 1
    for peak in peaks:
        # maybe always round left down and right up to enlarge interval a little?
        left_index = round((peak.allele.mid - peak.allele.left) * 10)
        right_index = round((peak.allele.mid + peak.allele.right) * 10)
        dye_index = peak.allele.dye.plot_index - 1
        # intervals are all about 1 nucleotide wide at most, 0.8 at least
        bin_edges[dye_index].append((left_index, right_index))
    return bin_edges  # list of left-right pairs (indices of left and right side) of each bin


def find_peaks_in_bins(sample: Sample, list_of_bin_indices: list):
    """Makes array of True/False of same size as data. True if a peak should theoretically be visible\
    based on the composition and the bin locations, False otherwise."""
    # Returns a 6xn numpy array
    indices = []
    for dye_color in range(6):
        bin_data = list_of_bin_indices[dye_color]
        sample_data = sample.data[:, dye_color]
        new_indices = [True if sample_data[ind] > 80 and ind in bin_data else False for ind in range(len(sample_data))]
        indices.append(new_indices)
    return np.array(indices)


def find_peaks_flowing_out_of_bins(sample: Sample, list_of_bin_sides: list):
    """Makes array of same size as data with True/False values if peak should be visible.
    Uses maximum within bin and follows whatever part of peak is visible to entire peak."""
    indices = []
    for color in range(6):
        bin_data = list_of_bin_sides[color]
        sample_data = sample.data[:, color]
        bin_booleans = [False] * len(sample_data)
        for left, right in bin_data:
            max_index = left + np.argmax(sample_data[left:right + 1])
            if sample_data[max_index - 1] > sample_data[max_index]:
                while sample_data[max_index - 1] - sample_data[max_index] > 1e-10:
                    max_index -= 1
            elif sample_data[max_index + 1] > sample_data[max_index]:
                while sample_data[max_index + 1] - sample_data[max_index] > 1e-10:
                    max_index += 1
            bin_booleans[max_index] = True
            left_end = max_index
            right_end = max_index
            while sample_data[left_end] - sample_data[left_end - 1] > 1e-10:
                left_end -= 1
                bin_booleans[left_end] = True
            while sample_data[right_end] - sample_data[right_end + 1] > 1e-10:
                right_end += 1
                bin_booleans[right_end] = True
        indices.append(bin_booleans)
    # array returned has same dimensions as sample array
    # correction: not same shape as array, but transposed
    # this will probably cause trouble in some other functions
    return np.array(indices).transpose()
