from src import data_prep_functions as dpf, plotting_functions as pf, reading_functions as rf, training_functions as trf
from src import classes as c
import pandas as pd
import numpy as np

tracedata = ['TraceDataSet11.txt', 'TraceDataSet12.txt', 'TraceDataSet21.txt', 'TraceDataSet22.txt',
             'TraceDataSet31.txt', 'TraceDataSet32.txt', 'TraceDataSet41.txt', 'TraceDataSet42.txt',
             'TraceDataSet51.txt', 'TraceDataSet52.txt', 'TraceDataSet61.txt', 'TraceDataSet62.txt']
# to speed up tests, only do first dataset
tracedata = ["TraceDataSet42.txt"]

def some_examples():
    # first create a list of all samples
    samples = []
    for elt in tracedata:
        samples += rf.txt_read_sample(elt)
    for sample in samples:
        current_name = sample.name
        # still contains pocons and ladders, so next loop filters this
        if len(current_name) == 3 and current_name != "3E2":
            person_mixture = rf.make_person_mixture(current_name)
            peak_booleans = dpf.find_peaks_flowing_out_of_bins(sample, dpf.bin_lefts_rights(person_mixture))
            peak_booleans_alt = dpf.find_peaks_in_bins(sample, dpf.bin_all_indices(person_mixture))
            # for dye_index in range(5):
            dye_index = 4
            pf.plot_labeled_background(sample.data[:, dye_index], peak_booleans[dye_index], dye_index)
            pf.plot_labeled_background(sample.data[:, dye_index], peak_booleans_alt[dye_index], dye_index)

if __name__ == '__main__':
    # some_examples()
    samples = rf.txt_read_sample(tracedata[0])
    first_sample = samples[6]
    first_name = first_sample.name
    person_mixture = rf.make_person_mixture(first_name)
    pf.plot_all_markers_and_bins()
    # first_input = dpf.create_input_from_sample(first_sample, 80, person_mixture, 5)
    # print((np.sum(first_input.labels,axis=0))/len(first_input.labels[:,0]))
    # print(trf.simplest_nn(first_input))

