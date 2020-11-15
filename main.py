import reading_functions as rf
import plotting_functions as pf


if __name__ == '__main__':
    sample_list = rf.txt_read_data('trace_data/TraceData1.txt')
    locus_dict = rf.xml_read_bins("PPF6C_SPOOR.xml")
    print(locus_dict)
    personlist = rf.csv_read_persons(1, locus_dict)
    mixt = rf.make_mixture(personlist, '1A2', locus_dict)
    pf.plot_actual('titel', mixt, locus_dict, sample_list[20])
