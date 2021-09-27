from src import data_prep_functions as dpf, plotting_functions as pf, reading_functions as rf, training_functions as trf, plotting_6C_functions as pf6, post_processing_functions as ppf, results as r
import numpy as np
import matplotlib.pyplot as plt


tracedata = ['TraceDataSet11.txt', 'TraceDataSet12.txt', 'TraceDataSet21.txt', 'TraceDataSet22.txt',
             'TraceDataSet31.txt', 'TraceDataSet32.txt', 'TraceDataSet41.txt', 'TraceDataSet42.txt',
             'TraceDataSet51.txt', 'TraceDataSet52.txt', 'TraceDataSet61.txt', 'TraceDataSet62.txt']


if __name__ == '__main__':
    samples = rf.txt_read_sample("TraceDataSet62.txt")
    samples = []
    for elt in tracedata:
        samples += rf.txt_read_sample(elt)
    leftoffset = 500
    rightcutoff = 4800 + 500
    number_of_dyes = 6
    original_sampledata, inputs_for_unet, sample_names = dpf.input_from_multiple_samples(samples, number_of_dyes, leftoffset, rightcutoff, True)

    unet_model = trf.unet(inputs_for_unet, rightcutoff - leftoffset, 'data/weights_norm_avgpool.h5', False)
    for index_of_sample in range(1):
        sample_data = original_sampledata[index_of_sample]
        sample_name = sample_names[index_of_sample].split(".")[0]
        input_example = inputs_for_unet.data[index_of_sample, :, :].reshape(1, rightcutoff - leftoffset, number_of_dyes, 1)
        output_example = unet_model.predict(input_example).reshape(4800, 6)
        label_example = inputs_for_unet.labels[index_of_sample, :, :]
        pf6.plot_results_unet(sample_data, output_example)
