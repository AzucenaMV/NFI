from src.classes import *


def input_maker(sample: Sample, width: int):
    """Takes Sample, returns list of Inputs"""
    # width is 80 or 200
    sample_data = sample.data
    input_list = []
    for i in range(len(sample_data)-width):
        window = sample_data[i: i + width+1, :].copy()
        center_location = (i + width + 1) / 10
        for index in range(6):
            new_center = Center(center_location, Dyes().color_list[index])
            new_input = TrainInput(sample.name + "_" + str(i) + "_" + str(index), window, new_center, 0)
            input_list.append(new_input)
    return input_list


def label_maker(person_mix, locus_dict):
    peaks = person_mix.create_peaks(locus_dict)
    label_list = [[], [], [], [], [], []]
    # cannot find precise index, since "size" of bins is accurate to 2 decimals, measurements to 1
    for peak in peaks:
        # should i also add approximate height in some way?
        x_val = round(peak.x*10)      # approximate index of peak
        dye_index = peak.dye.plot_index - 1
        # intervals are all about 1 nucleotide wide at most, 0.8 at least
        label_list[dye_index].append(x_val)
        # now assumes bin size of 0.4 in both directions, actually wrong...
        for i in range(4):
            label_list[dye_index].append(x_val-i-1)
        for i in range(4):
            label_list[dye_index].append(x_val+i+1)
    return label_list   # has indices of peaks per dye -> Why indices?


def labeler(input_list, label_list):
    """Combines input list with label list for labeled entries"""
    for i in range(len(input_list)):
        if i + 41 in label_list[i % 6]:         # 41 steps from start is midpoint to be labeled
            input_list[i].label = 1             # always set to 1?
        else:
            input_list[i].label = 0
    return input_list
