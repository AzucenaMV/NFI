from src import data_prep_functions as df, plotting_functions as pf, reading_functions as rf
from src import classes as c
import pandas as pd

tracedata = ['TraceDataSet11.txt', 'TraceDataSet12.txt', 'TraceDataSet21.txt', 'TraceDataSet22.txt',
             'TraceDataSet31.txt', 'TraceDataSet32.txt', 'TraceDataSet41.txt', 'TraceDataSet42.txt',
             'TraceDataSet51.txt', 'TraceDataSet52.txt', 'TraceDataSet61.txt', 'TraceDataSet62.txt']
# to speed up tests, only do first dataset
tracedata = ["TraceDataSet51.txt"]

def some_examples():
    # first create a list of all samples
    samples = []
    for elt in tracedata:
        samples += rf.txt_read_sample(elt)
    for sample in samples:
        current_name = sample.name
        #pf.plot_sample_markers_6C(sample)
        if len(current_name) == 3 and current_name != "3E2":
            person_mixture = rf.make_person_mixture(current_name)
            peaks = person_mixture.create_peaks()
            peak_booleans = df.find_peaks_flowing_out_of_bins(sample, df.bin_finder(person_mixture))
            # peak_booleans = df.find_peaks_in_bins(sample, df.bin_indices_maker(person_mixture))
            pf.plot_background(sample.data[:,0], peak_booleans)
            pf.plot_labeled_sample(sample.data[:,0], peak_booleans)

if __name__ == '__main__':
    some_examples()

