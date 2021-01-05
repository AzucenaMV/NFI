from src.classes import *


# should have approximately that shape, but need to decide what to do about other colours.
def create_input_from_sample(sample: Sample, width: int, person_mix):
    """For one electropherogram, creates all input (node) images and their labels."""
    # width is amount of steps in each direction, either 80 or 100
    sample_data = sample.data
    window_list = []
    labels = find_peaks_in_bins(sample, bin_all_indices(person_mix))
    label_list = []
    for i in range(len(sample_data)-2*width):
        window = sample_data[i: i + 2*width+1, :].copy()
        center_location = i + width + 1
        window_list.append(window)
        label_list.append(labels[:,center_location])
    input_from_sample = TrainInput(sample, window_list, label_list)
    return input_from_sample


def bin_all_indices(person_mix):
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


def bin_lefts_rights(person_mix):
    """Makes list of left and right sides of allelebins when expected"""
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
    return bin_edges   # has indices of left and right side of each bin


def find_peaks_in_bins(sample: Sample, list_of_bins: list):
    """Makes array of True/False of same size as data. True if a peak should theoretically be visible\
    based on the composition and the bin locations, False otherwise."""
    # Returns a 6xn numpy array
    indices = []
    for dye_color in range(6):
        dye_data = list_of_bins[dye_color]
        sample_data = sample.data[:,dye_color]
        new_indices = [True if sample_data[ind] > 80 and ind in dye_data else False for ind in range(len(sample_data))]
        indices.append(new_indices)
    return np.array(indices)


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


def labeler(width, sample, person_mix):
    """Creates list of 6x1 arrays of labels per window"""
    # width is amount of pixels to left and right of pixel to be labeled
    return []
