from src.classes import *


def window_maker(sample: Sample, width: int):
    """Takes Sample, returns Input"""
    # width is 80 or 200
    sample_data = sample.data
    input_list = []
    for i in range(len(sample_data)-width):
        input_data = sample_data[i: i + width+1, :].copy()
        center = i + width + 1
        new_input = TrainInput(sample.name + "_" + str(i), input_data, center, "")
        input_list.append(new_input)
    return input_list


def label_maker(person_mix, locus_dict):
    peaks = person_mix.create_peaks(locus_dict)
    label_list = []
    for peak in peaks:
        x_val = round(peak.x*10)      # approximate index of peak
        # intervals are all about 1 nucleotide wide at most, 0.8 at least
        label_list.append(x_val)
        for i in range(4):
            label_list.append(x_val-i-1)
        for i in range(4):
            label_list.append(x_val+i+1)
    return label_list   # has indices of peaks


def labeler(input_list, label_list):
    """Combines input list with label list for labeled entries"""
    for i in range(len(input_list)):
        input_list[i].label = label_list[i]
    return input_list
