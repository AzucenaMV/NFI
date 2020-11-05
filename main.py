import reading_functions as rf
import plotting_functions as pf

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sizedtitles, sizedcolors, sizeddata = rf.txt_read_data('SizedTraceData.txt')
    # allele_dict contains bins for each allele (e.g. AMEL: {X: 81.5, Y: 87.68})
    # dye_dict contains the color of each dye name (e.g. FL: 'b')
    allele_dict, dye_dict = rf.xml_read_bins("PPF6C_SPOOR.xml")

