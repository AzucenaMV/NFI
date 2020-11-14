import reading_functions as rf
import plotting_functions as pf
from GLOBALS import *


if __name__ == '__main__':
    sample_list = rf.txt_read_data('TraceData1.txt')
    locus_dict = rf.xml_read_bins("PPF6C_SPOOR.xml")
    print(locus_dict)
    personlist = rf.csv_read_persons(1, locus_dict)
    print(rf.make_mixture(personlist, '1A2', locus_dict))
