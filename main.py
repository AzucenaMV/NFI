from dataclasses import dataclass
from typing import List

import reading_functions as rf
import plotting_functions as pf

@dataclass
class Dye:
    name: str
    plot_color: str
    pos: int

@dataclass
class Allele:
    midpoint: int
    name: str

@dataclass
class Locus:
    alleles: List[Allele]
    name: str
    dye: Dye

# class voor:
# mengsel (gemeten waarde) (wel rfu)
# persoon (theoretische waarde) (geen rfu, maar allelen)
# (ook wat analyst heeft aangewezen?)

# misschien uiteindelijk:
# output class/geanalyseerd profiel, welke pieken zijn aangewezen door CNN


if __name__ == '__main__':
    sizedtitles, sizedcolors, sizeddata = rf.txt_read_data('SizedTraceData.txt')
    # allele_dict contains bins for each allele (e.g. AMEL: {X: 81.5, Y: 87.68})
    # dye_dict contains the color of each dye name (e.g. FL: 'b')
    allele_dict, dye_dict, empty_dict = rf.xml_read_bins("PPF6C_SPOOR.xml")
    # resulting_dict = rf.csv_read_actual('donor_profiles/Refs_dataset2.csv', '2A5', empty_dict)
    allele_list, height_list = rf.csv_read_analyst("analysts_data_filtered/1A2_New.csv")
    alleles_actual = rf.csv_read_actual("donor_profiles/Refs_dataset1.csv", "1A2", empty_dict)
    pf.plot_actual("1A2.1",alleles_actual, allele_dict, dye_dict, sizeddata[:,36:42])