import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src import plotting_6C_functions as pf6
from src.classes import *

files_3130_mix = ["3130 mixture - test profiles/889-09_400pg_4-1_B02_004.csv", "3130 mixture - test profiles/889-21_400pg_3-2-1_F03_011.csv", "3130 mixture - test profiles/889-37_200pg_5-1_F05_011.csv", "3130 mixture - test profiles/889-37_200pg_5-1_F05_011.csv", "3130 mixture - test profiles/890_09_10pg_1-1-1-1_B02_004.csv"]
files_3130_ref = ["3130 references - test profiles/1 - 449753.csv", "3130 references - test profiles/2 - 449755.csv", "3130 references - test profiles/3 - 449746.csv", "3130 references - test profiles/4 - 449756.csv", "3130 references - test profiles/5 - 449742.csv"]
files_3500_mix = ["3500 mixture - test profiles/18_1000_5-4-3-2-1_B03_06.csv", "3500 mixture - test profiles/33_400_50-25-10-1_A05_02.csv", "3500 mixture - test profiles/35_100_50-25-10-1_C05_08.csv", "3500 mixture - test profiles/41_200_5-4-3-2-1_A06_03.csv" ]
files_3500_ref = ["3500 references - test profiles/08_3500xl_01_P986_06_20ng_to_1ng_H01_22.csv", "3500 references - test profiles/16_3500xl_01_P986_04_5ng_to_250pg_H02_23.csv", "3500 references - test profiles/478128_1703725__C01_07.csv", "3500 references - test profiles/478145_1703795__D03_12.csv", "3500 references - test profiles/478253_1702694__E03_15.csv"]

all_files = files_3130_mix+files_3130_ref+files_3500_mix+files_3500_ref

def read_csv_DTDP(filename = "3130 references - test profiles/1 - 449753.csv", folder = "data/DTDP_profiles/"):
    dataframe = pd.read_csv(folder + filename)
    data = np.array(dataframe[['dye1', 'dye2', 'dye3', 'dye4', 'dye6', 'dye5']].values)     # need to swap 5 and 6 to get size std at bottom
    labels_multi = np.array(dataframe[['dye1GT', 'dye2GT', 'dye3GT', 'dye4GT', 'dye6GT', 'dye5GT']].values)
    labels_binary = np.isin(labels_multi, 'A')  # label 'A' is reserved for alleles
    range_start = 3750
    # pf6.plot_inputs_unet(data[range_start:9000, :], labels_binary[range_start:9000,:], rescale=12)
    return data[range_start:range_start+4800, :], labels_binary[range_start:range_start+4800, :]


def find_marker_ranges_DTDP():
    """temporary function to check where allees end and start"""
    for filename in all_files:
        dataframe = pd.read_csv("data/DTDP_profiles/"+filename)
        data = np.array(dataframe[['dye1', 'dye2', 'dye3', 'dye4', 'dye6',
                               'dye5']].values)  # need to swap 5 and 6 to get size std at bottom
        labels_multi = np.array(dataframe[['dye1GT', 'dye2GT', 'dye3GT', 'dye4GT', 'dye6GT', 'dye5GT']].values)
        labels_binary = np.where(labels_multi == 'A')
        # print(labels_binary[0][0], labels_binary[0][-1])
    pass


def input_from_DTDP(normalised = True, filenames = all_files):
    original_data = []
    input_data = []
    input_labels = []
    for filename in filenames:
        unnormalised_data, labels = read_csv_DTDP(filename)
        input_labels.append(labels)
        new = unnormalised_data - np.min(unnormalised_data)
        normalised_data = new / 10000   # theoretical max of 3130 data
        input_data.append(normalised_data)
        original_data.append(unnormalised_data)
    if normalised:
        inputs = TrainInput(np.array(input_data), np.array(input_labels))
    else:
        inputs = TrainInput(np.array(original_data), np.array(input_labels))
    return original_data, inputs


