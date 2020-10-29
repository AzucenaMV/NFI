import reading_functions as rf

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sized_titles, sized_colors, sized_data = rf.read_func('SizedTraceData.txt')
    raw_titles, raw_colors, raw_data = rf.read_func('RawTraceData.txt')
    rf.plot_compare(raw_data,sized_data,sized_titles,sized_colors)

