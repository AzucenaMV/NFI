from src import data_prep_functions as dpf, plotting_functions as pf, reading_functions as rf, training_functions as trf, plotting_6C_functions as pf6, post_processing_functions as ppf
from src import classes as c
import numpy as np
from src import models

tracedata = ['TraceDataSet11.txt', 'TraceDataSet12.txt', 'TraceDataSet21.txt', 'TraceDataSet22.txt',
             'TraceDataSet31.txt', 'TraceDataSet32.txt', 'TraceDataSet41.txt', 'TraceDataSet42.txt',
             'TraceDataSet51.txt', 'TraceDataSet52.txt', 'TraceDataSet61.txt', 'TraceDataSet62.txt']
# to speed up tests, only do first dataset
# tracedata = ["TraceDataSet11.txt"]

def some_examples():
    # first create a list of all samples
    samples = []
    for elt in tracedata:
        samples += rf.txt_read_sample(elt)
    leftoffset = 500
    cutoff = 4800 + 500
    number_of_dyes = 6
    original_sampledata, inputs_for_unet, sample_names = dpf.input_from_multiple_samples(samples, number_of_dyes, leftoffset, cutoff, True)
    unet_model = trf.unet(inputs_for_unet, cutoff - leftoffset, 'weights_norm_avgpool.h5', False)

    for sample_number in range(len(sample_names)):
        sample_name = sample_names[sample_number]
        sample_data = original_sampledata[sample_number]
        # has been normalised
        input_example = inputs_for_unet.data[sample_number,:,:].reshape(1,cutoff-leftoffset,number_of_dyes,1)
        # labels
        label_example = inputs_for_unet.labels[sample_number, :, :]
        # pf6.plot_bins_vs_labels(sample_data, dpf.find_peaks_in_bins(sample_data, sample_name), label_example, "Bins_vs_peaks_" + sample_name)
        # result of u-net
        # output_example = unet_model.predict(input_example).reshape(4800,6)
        # print(ppf.IOU(label_example, output_example))
        # ppf.print_all_peaks(sample_name)
        # ppf.pixels_to_peaks(sample_data, output_example, 0.5, leftoffset, sample_name)
        # pf6.plot_results_unet_against_truth(sample_data, output_example, label_example)
        # pf6.plot_results_unet_against_truth_alt(sample_data, output_example, label_example)


def old_examples():
    samples = []
    for elt in tracedata:
        samples += rf.txt_read_sample(elt)
    for sample in samples:
        current_name = sample.name
        # still contains pocons and ladders, so next loop filters this
        if len(current_name) == 3 and current_name != "3E2":
            person_mixture = rf.make_person_mixture(current_name)
            peak_booleans = dpf.find_peaks_flowing_out_of_bins(sample)
            # peak_booleans_alt = dpf.find_peaks_in_bins(sample)
            # for dye_index in range(5):
            dye_index = 4
            pf.plot_labeled_background(sample.data[:, dye_index], peak_booleans[dye_index], dye_index)
            # pf.plot_labeled_background(sample.data[:, dye_index], peak_booleans_alt[dye_index], dye_index)

if __name__ == '__main__':
    some_examples()


