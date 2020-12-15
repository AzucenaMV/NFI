from src import data_prep_functions as df, plotting_functions as pf, reading_functions as rf
from src import classes as c
import pandas as pd

tracedata = ['TraceDataSet11.txt', 'TraceDataSet12.txt', 'TraceDataSet21.txt', 'TraceDataSet22.txt',
             'TraceDataSet31.txt', 'TraceDataSet32.txt', 'TraceDataSet41.txt', 'TraceDataSet42.txt',
             'TraceDataSet51.txt', 'TraceDataSet52.txt', 'TraceDataSet61.txt', 'TraceDataSet62.txt']


def some_examples():
    # first create a list of all samples
    samples = []
    for elt in tracedata:
        samples += rf.txt_read_sample(elt)
    for sample in samples[20:21]:
        current_name = sample.name
        #pf.plot_sample_markers_6C(sample)
        if len(current_name) == 3 and current_name != "3E2":
            replicas = rf.csv_read_analyst(current_name)
            # pf.plot_analyst(replicas[sample.replica - 1].peaks, sample)
            person_mixture = rf.make_person_mixture(current_name)
            peaks = person_mixture.create_peaks()
            pf.plot_expected(peaks, sample)


if __name__ == '__main__':
    some_examples()
    # samples = rf.txt_read_sample(tracedata[0])
    # for i in range(2):
    #     sample = samples[i]
    #     if len(sample.name) == 3:
    #         person_mix = rf.make_person_mixture(sample.name)
    #         peaks = person_mix.create_peaks()
    #         number_of_peaks = len(peaks)
    #     else:
    #         peaks = []
    #     only_blue, peak_bools = df.find_peak_locations(sample)
    #     pf.plot_background(only_blue, peak_bools)
    #     pf.plot_labeled_sample(only_blue, peak_bools)

