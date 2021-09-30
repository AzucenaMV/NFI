from src import data_prep_functions as dpf, plotting_functions as pf, reading_functions as rf, training_functions as trf, plotting_6C_functions as pf6, writing_functions as wf, post_processing_functions as ppf, results as r, reading_data_DTDP as rdD
import numpy as np
import matplotlib.pyplot as plt


# tracedata = ['TraceDataSet11.txt', 'TraceDataSet12.txt', 'TraceDataSet21.txt', 'TraceDataSet22.txt',
#              'TraceDataSet31.txt', 'TraceDataSet32.txt', 'TraceDataSet41.txt', 'TraceDataSet42.txt',
#              'TraceDataSet51.txt', 'TraceDataSet52.txt', 'TraceDataSet61.txt', 'TraceDataSet62.txt']

tracedata_for_training = ['TraceDataSet11.txt', 'TraceDataSet12.txt', 'TraceDataSet21.txt', 'TraceDataSet22.txt',
             'TraceDataSet31.txt', 'TraceDataSet32.txt', 'TraceDataSet41.txt', 'TraceDataSet42.txt',
             'TraceDataSet51.txt', 'TraceDataSet52.txt']
tracedata_for_testing = ['TraceDataSet61.txt', 'TraceDataSet62.txt']

#
if __name__ == '__main__':
    number_of_dyes = 6

    # unnormalised_test_input, normalised_test_input = rdD.input_from_DTDP()
    # length = 4800
    # unet_model_DTDP = trf.unet_train_test_split([], normalised_test_input, length, weightpath="data/weights_NFI/weights_6_split.h5", train=False)
    # for index_of_sample in range(15,19):
    #     sample_data = unnormalised_test_input[index_of_sample]
    #     input_example = normalised_test_input.data[index_of_sample, :, :].reshape(1, length, number_of_dyes, 1)
    #     output_example = unet_model_DTDP.predict(input_example).reshape(length, 6)
    #     label_example = normalised_test_input.labels[index_of_sample, :, :]
    #     pf6.plot_results_unet_against_truth(sample_data, output_example, label_example)

    leftoffset = 500
    rightcutoff = 4800 + 500
    train_samples = []
    for elt in tracedata_for_training:
        train_samples += rf.txt_read_sample(elt)
    test_samples = []
    for elt in tracedata_for_testing:
        test_samples += rf.txt_read_sample(elt)
    unnormalised_train_data, train_input, train_sample_names = dpf.input_from_multiple_samples(train_samples, number_of_dyes, leftoffset, rightcutoff, True)
    unnormalised_test_data, test_input, test_sample_names = dpf.input_from_multiple_samples(test_samples, number_of_dyes, leftoffset, rightcutoff, True)

    # print(test_samples[15].name)
    # print(test_samples[20].name)
    # DTDP_train_input = dpf.create_DTDP_inputs_from_sample(test_samples[15], 100, number_of_dyes)
    # DTDP_test_input = dpf.create_DTDP_inputs_from_sample(test_samples[20], 100, number_of_dyes)
    # FFN_model = trf.FFN(DTDP_train_input, DTDP_test_input, train = True)
    # check_shape = FFN_model.predict(test_samples[20].data[0])
    # print(check_shape.shape)

    unet_model = trf.unet_train_test_split(train_input, test_input, rightcutoff - leftoffset, weightpath='data/weights_NFI/weights_6_split_new.h5', train=False)
    for index_of_sample in range(1):
        sample_data = unnormalised_test_data[index_of_sample]
        sample_name = test_sample_names[index_of_sample].split(".")[0]
        input_example = test_input.data[index_of_sample, :, :].reshape(1, rightcutoff - leftoffset, number_of_dyes, 1)
        output_example = unet_model.predict(input_example).reshape(4800, 6)
        label_example = test_input.labels[index_of_sample, :, :]
        pf6.plot_results_unet_against_truth(input_example, output_example, label_example)
