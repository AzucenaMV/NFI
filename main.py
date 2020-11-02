import reading_functions as rf

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    allelelist, heightlist = rf.csv_read_analyst("1A2_New.csv")
    alleledict, dyedict = rf.xml_read_bins("PPF6C_SPOOR.xml")
    print(dyedict)
    rf.plot_actual(allelelist[0], heightlist[0], alleledict, dyedict)
