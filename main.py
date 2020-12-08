from src import data_prep_functions as df, plotting_functions as pf, reading_functions as rf
from src import classes as c
import pandas as pd

tracedata = ['TraceDataSet11.txt', 'TraceDataSet12.txt', 'TraceDataSet21.txt', 'TraceDataSet22.txt',
             'TraceDataSet31.txt', 'TraceDataSet32.txt', 'TraceDataSet33.txt', 'TraceDataSet41.txt',
             'TraceDataSet42.txt', 'TraceDataSet51.txt', 'TraceDataSet52.txt', 'TraceDataSet61.txt',
             'TraceDataSet62.txt']


def some_examples():
    # first create a list of all samples
    samples_cis = []
    samples_mine = []
    samples, names_cis = rf.txt_read_data("data/trace_data/TraceData1.txt")
    samples_cis += samples
    set_names_cis = set(names_cis)
    samples, names = rf.txt_read_data("data/trace_data/TraceData2.txt")
    samples_cis += samples
    set_names_cis.update(set(names))
    names_cis += names
    samples, names_mine = rf.txt_read_data("data/trace_data/" + tracedata[0])
    samples_mine += samples
    set_names_mine = set(names_mine)
    samples, names = rf.txt_read_data("data/trace_data/" + tracedata[1])
    samples_mine += samples
    set_names_mine.update(set(names))
    names_mine += names
    print("Names of your dataset (in order): ", names_cis)
    print("Names of my dataset (in order): ", names_mine)
    print("What is in yours, but not in mine", set_names_cis - set_names_mine)
    print("What is in mine but not in yours", set_names_mine - set_names_cis)
    locus_dict = rf.xml_read_bins()
    # for i in range(10, 11):
    #     cis = samples_cis[i]
    #     mine = samples_mine[i]
    #     current_name = cis.name
    #     pf.plot_sample_markers_6C(cis, locus_dict)
    #     pf.plot_sample_markers_6C(mine, locus_dict)
    #     replicas = rf.csv_read_analyst(current_name, locus_dict)
    #     pf.plot_analyst_6C(replicas[cis.replica - 1].peaks, cis, locus_dict)
    #     pf.plot_analyst_6C(replicas[mine.replica - 1].peaks, mine, locus_dict)
    #     person_mixture = rf.make_person_mixture(current_name)
    #     peaks = person_mixture.create_peaks(locus_dict)
    #     pf.plot_expected_6C(peaks, cis, locus_dict)
    #     pf.plot_expected_6C(peaks, mine, locus_dict)



if __name__ == '__main__':
