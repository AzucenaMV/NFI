import reading_functions as rf
import plotting_functions as pf
from GLOBALS import *


if __name__ == '__main__':
    sample_list = rf.txt_read_data('SizedTraceData.txt')
    # allele_dict contains bins for each allele (e.g. AMEL: {X: 81.5, Y: 87.68})
    # dye_dict contains the color of each dye name (e.g. FL: 'b')
    allele_dict, dye_dict, empty_dict = rf.xml_read_bins("PPF6C_SPOOR.xml")
