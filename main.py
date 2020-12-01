from src import data_prep_functions as df, plotting_functions as pf, reading_functions as rf
from src import classes as c

if __name__ == '__main__':
    samp = rf.txt_read_data("data/trace_data/TraceData1.txt")[30]
    locus_dict = rf.xml_read_bins()
    person_mix = rf.make_person_mixture(samp.name, locus_dict)
    inputs = df.window_maker(samp, 80)
    labels = df.label_maker(person_mix, locus_dict)
    labeled_inputs = df.labeler(inputs, labels)


def some_examples():
    # first create a list of all samples
    sample_list_1 = rf.txt_read_data("data/trace_data/TraceData1.txt")
    sample_list_2 = rf.txt_read_data("data/trace_data/TraceData2.txt")
    sample_list = sample_list_1 + sample_list_2
    # now we get all panel information from the Genemarker file
    locus_dict = rf.xml_read_bins()
    # plot some samples with marker bins
    for i in range(10, 13):
        current = sample_list[i]
        current_name = current.name
        pf.plot_sample_markers_6C(current, locus_dict)
        # Everything underneath
        # plot samples with analyst's identified peaks
        replicas = rf.csv_read_analyst(current_name, locus_dict)
        # now have a list of the analyst's identified peaks + heights for all replicates
        # currently always picks first replica
        pf.plot_analyst_6C(replicas[0].peaks, current, locus_dict)
        # now plot with actual peaks
        peaks = rf.make_person_mixture(current_name, locus_dict)
        pf.plot_expected_6C(peaks, current, locus_dict)
    pass