import reading_functions as rf

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rawdata = rf.read_data('RawTraceData.txt')
    sizedtitles, sizedcolors, sizeddata = rf.read_data('SizedTraceData.txt')
    colors  = sizedcolors[0:6]
    data_A2_1 = sizeddata[:,36:42]
    data_A2_2 = sizeddata[:,42:48]
    data_A2_3 = sizeddata[:,48:54]
    allelelist, heightlist = rf.csv_read_analyst("1A2_New.csv")
    alleledict, dyedict = rf.xml_read_bins("PPF6C_SPOOR.xml")
    peaks_A2_1, peaks_A2_2, peaks_A2_3 = allelelist
    heights_A2_1, heights_A2_2, heights_A2_3 = heightlist
    rf.plot_actual(peaks_A2_1, heights_A2_1, alleledict, dyedict, data_A2_1, colors)
    #rf.plot_actual(peaks_A2_2, heights_A2_2, alleledict, dyedict, data_A2_2, colors)
    #rf.plot_actual(peaks_A2_3, heights_A2_3, alleledict, dyedict, data_A2_3, colors)
