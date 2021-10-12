from src import data_prep_functions as dpf, plotting_functions as pf, reading_functions as rf, training_functions as trf, plotting_6C_functions as pf6, writing_functions as wf, post_processing_functions as ppf, results as r, reading_data_DTDP as rdD
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.metrics import binary_crossentropy, binary_accuracy


tracedata_for_training = ['TraceDataSet11.txt', 'TraceDataSet12.txt', 'TraceDataSet21.txt', 'TraceDataSet22.txt',
             'TraceDataSet31.txt', 'TraceDataSet32.txt', 'TraceDataSet41.txt', 'TraceDataSet42.txt',
             'TraceDataSet51.txt', 'TraceDataSet52.txt']
tracedata_for_testing = ['TraceDataSet61.txt', 'TraceDataSet62.txt']

PROVEDIT_tracedata = ['PROVEDIt_RD14-0003(010616CMG_15sec)_sized1.txt','PROVEDIt_RD14-0003(010616CMG_15sec)_sized2.txt', 'PROVEDIt_RD14-0003(010616CMG_15sec)_sized3.txt', 'PROVEDIt_RD14-0003(020216ADG_15sec)_sized1.txt', 'PROVEDIt_RD14-0003(020216ADG_15sec)_sized2.txt', 'PROVEDIt_RD14-0003(021716ADG_15sec)_sized1.txt', 'PROVEDIt_RD14-0003(021716ADG_15sec)_sized2.txt', 'PROVEDIt_RD14-0003(021716ADG_15sec)_sized3.txt', 'PROVEDIt_RD14-0003(022516ADG_15sec)_sized1.txt', 'PROVEDIt_RD14-0003(022516ADG_15sec)_sized2.txt', 'PROVEDIt_RD14-0003(022516ADG_15sec)_sized3.txt', 'PROVEDIt_RD14-0003(100515ADG_15sec)_sized1.txt', 'PROVEDIt_RD14-0003(100515ADG_15sec)_sized2.txt']

#
if __name__ == '__main__':
    number_of_dyes = 6
    # unnormalised_test_input_3130, normalised_test_input_3130 = rdD.input_3130_from_DTDP()
    # unnormalised_test_input_3500, normalised_test_input_3500 = rdD.input_3500_from_DTDP()

    leftoffset = 500
    rightcutoff = 4800 + 500
    # train_samples = []
    # for elt in tracedata_for_training:
    #     train_samples += rf.txt_read_sample(elt)
    # test_samples = []
    # for elt in tracedata_for_testing:
    #     test_samples += rf.txt_read_sample(elt)
    # unnormalised_train_data, train_input, train_sample_names = dpf.input_from_multiple_samples(train_samples, number_of_dyes, leftoffset, rightcutoff, True)
    # unnormalised_test_data, test_input, test_sample_names = dpf.input_from_multiple_samples(test_samples, number_of_dyes, leftoffset, rightcutoff, True)
    # # Unet = trf.unet_train_test_split(train_input, test_input, 4800, "data/weights_NFI/weights_6_split.h5", train=False, epochs = 100)
    # # trf.unet_train_test_split(train_input, test_input, 4800, "data/weights_NFI/weights_6_split_new.h5", train=False, epochs=100)
    # Unet = trf.unet_train_test_split(train_input, test_input, 4800, "data/weights_NFI/weights_6_split_300epochs+LRs100.h5", train=False,epochs=100)
    PROVEDIt_samples = []
    for elt in PROVEDIT_tracedata:
        PROVEDIt_samples += rf.txt_read_sample_PROVEDIt(elt)
    originals, PROVEDIt_input, names = dpf.input_from_multiple_PROVEDIt_samples(PROVEDIt_samples, number_of_dyes, leftoffset, rightcutoff, True)
    for data_index in range(200,205):
        pf6.plot_inputs_PROVEDIt(PROVEDIt_input.data[data_index])
    # trf.unet_train_test_split([], PROVEDIt_input, rightcutoff-leftoffset, "data/weights_NFI/weights_6_split_300epochs+LRs100.h5", train=False)



    # width = 80
    # input_dim = 6*(width*2+1)
    # DTDP_train_input = dpf.DTDP_input_from_multiple_samples(train_samples, width = width)
    # DTDP_test_input = dpf.DTDP_input_from_multiple_samples(test_samples, width = width)
    # FFN_model = trf.FFN(DTDP_train_input, DTDP_test_input, weightpath="data/weights_DTDP/weights_FFN_our_data_w80_100epochs.h5", inputsize=(input_dim,), train = False, epochs=100, batchsize=100)
    # # images, prediction = ppf.combine_results_FFN(DTDP_test_input, test_input, FFN_model, input_dim)
    #
    # for index_of_image in range(test_input.data.shape[0]):
    #     input = test_input.data[index_of_image]
    #     prediction = Unet.predict(input.reshape(1,4800,6))
    #     pf.plot_results_FFN(input[:,0], prediction[:,:,0], test_input.labels[index_of_image,:,0], "Unet_fully_trained_on_"+test_sample_names[index_of_image])

