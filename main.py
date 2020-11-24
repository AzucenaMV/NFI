import reading_functions as rf
import plotting_functions as pf
import data_prep_functions as df

if __name__ == '__main__':
    samples = rf.txt_read_data("trace_data/TraceData1.txt")
    windows80 = df.window_maker(samples[2], 80)


def test_read_plot():
    # first create a list of all samples
    sample_list_1 = rf.txt_read_data("trace_data/TraceData1.txt")
    sample_list_2 = rf.txt_read_data("trace_data/TraceData2.txt")
    sample_list = sample_list_1 + sample_list_2
    # now we get all panel information from the Genemarker file
    locus_dict = rf.xml_read_bins()
    # plot samples with marker bins
    for i in range(10, 13):
        current = sample_list[i]
        current_name = current.name
        pf.plot_sample_markers_6C(current, locus_dict)
        # Everything underneath
        # plot samples with analyst's identified peaks
        replicas = rf.csv_read_analyst(current_name, locus_dict)
        # now have a list of the analyst's identified peaks + heights for all replicates
        # currently always picks first replica, since no way to know which is correct
        pf.plot_analyst_6C(replicas[0].peaks, current, locus_dict)
        # now plot with actual peaks
        peaks = rf.make_person_mixture(current_name, locus_dict)
        pf.plot_expected_6C(peaks, current, locus_dict)
    pass