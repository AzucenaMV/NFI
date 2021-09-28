from src import data_prep_functions as dpf, plotting_functions as pf, reading_functions as rf, training_functions as trf, plotting_6C_functions as pf6, post_processing_functions as ppf, results as r, reading_data_DTDP as rdD
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

    unnormalised_train_input, normalised_train_input = rdD.input_from_DTDP(filenames=["3130 mixture - test profiles/889-09_400pg_4-1_B02_004.csv", "3130 mixture - test profiles/889-21_400pg_3-2-1_F03_011.csv", "3130 mixture - test profiles/889-37_200pg_5-1_F05_011.csv", "3130 mixture - test profiles/889-37_200pg_5-1_F05_011.csv", "3130 mixture - test profiles/890_09_10pg_1-1-1-1_B02_004.csv", "3130 references - test profiles/1 - 449753.csv", "3130 references - test profiles/2 - 449755.csv", "3130 references - test profiles/3 - 449746.csv"])
    length = 6000
    unnormalised_test_input, normalised_test_input = rdD.input_from_DTDP(filenames=["3130 references - test profiles/4 - 449756.csv", "3130 references - test profiles/5 - 449742.csv"])
    unet_model_DTDP = trf.unet_train_test_split(normalised_train_input, normalised_test_input, length, weightpath="data/weights_DTDP/first_weights.h5", train=True)
    for index_of_sample in range(2):
        sample_data = unnormalised_test_input[index_of_sample]
        input_example = normalised_test_input.data[index_of_sample, :, :].reshape(1, length, number_of_dyes, 1)
        output_example = unet_model_DTDP.predict(input_example).reshape(length, 6)
        label_example = normalised_test_input.labels[index_of_sample, :, :]
        pf6.plot_results_unet_against_truth(sample_data, output_example, label_example)

    # leftoffset = 500
    # rightcutoff = 4800 + 500
    # train_samples = []
    # for elt in tracedata_for_training:
    #     train_samples += rf.txt_read_sample(elt)
    # test_samples = []
    # for elt in tracedata_for_testing:
    #     test_samples += rf.txt_read_sample(elt)
    # unnormalised_train_data, train_input, train_sample_names = dpf.input_from_multiple_samples(train_samples, number_of_dyes, leftoffset, rightcutoff, True)
    # unnormalised_test_data, test_input, test_sample_names = dpf.input_from_multiple_samples(test_samples, number_of_dyes, leftoffset, rightcutoff, True)
    # unet_model = trf.unet_train_test_split(train_input, test_input, rightcutoff - leftoffset, weightpath='data/weights_NFI/weights_6_split.h5', train=False)
    # for index_of_sample in range(1):
    #     sample_data = unnormalised_test_data[index_of_sample]
    #     sample_name = test_sample_names[index_of_sample].split(".")[0]
    #     input_example = test_input.data[index_of_sample, :, :].reshape(1, rightcutoff - leftoffset, number_of_dyes, 1)
    #     output_example = unet_model.predict(input_example).reshape(4800, 6)
    #     label_example = test_input.labels[index_of_sample, :, :]
    #     pf6.plot_results_unet_against_truth(sample_data, output_example, label_example)
