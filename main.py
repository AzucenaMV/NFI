import reading_functions as rf
import plotting_functions as pf
from classes import *

if __name__ == '__main__':
    # first create a list of all samples
    sample_list = rf.txt_read_data("trace_data/TraceData1.txt")
    sample_list.append(rf.txt_read_data("trace_data/TraceData2.txt"))
    locus_dict = rf.xml_read_bins("PPF6C_SPOOR.xml")
    mix_name = "1A2"
    donor_set, mixture_type, donor_amount = mix_name
    # just a small thing, but always need to convert this one to int, \
    # better to do in function or outside of function and specify it needs
    # to be an int in the function?
    donor_amount = int(donor_amount)
    peaks = rf.csv_read_analyst("analysts_data_filtered/1C3_New.csv")
    # should I make a function to do steps to create person mixture?
    # personlist = rf.csv_read_persons(donor_set)
    # personfracs, persons = rf.person_contributions(personlist, donor_amount, mixture_type)
    # person_mix = PersonMixture(mix_name, persons, personfracs)
    # peaks = person_mix.create_peaks(locus_dict)
    pf.plot_analyst(mix_name,peaks, sample_list[20])