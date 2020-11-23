from classes import *


def window_maker_200(sample: Sample):
    """Takes Sample, returns list of Inputs"""
    sample_data = sample.data
    input_list = []
    for i in range(len(sample_data)-200):
        input_data = sample_data[i: i + 201, :].copy()
        new_input = TrainInput(sample.name + "_" + str(i), input_data)
        input_list.append(new_input)
    return input_list

def window_maker_80(sample: Sample):
    """Takes Sample, returns list of Inputs"""
    sample_data = sample.data
    input_list = []
    for i in range(len(sample_data)-80):
        input_data = sample_data[i: i + 81, :].copy()
        new_input = TrainInput(sample.name + "_" + str(i), input_data)
        input_list.append(new_input)
    return input_list