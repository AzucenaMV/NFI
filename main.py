from src import scores as s, data_prep_functions as dpf, plotting_functions as pf, reading_functions as rf, training_functions as trf, plotting_6C_functions as pf6, write_to_csv as wf, post_processing_functions as ppf, results as r, OLD_reading_data_DTDP as rdD
from src.models import MHCNN_DT, unet_small
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.metrics import BinaryAccuracy, AUC
import pandas as pd
from src import classes
from datetime import datetime


tracedata_for_training = ['TraceDataSet11.txt', 'TraceDataSet12.txt', 'TraceDataSet21.txt', 'TraceDataSet22.txt',
             'TraceDataSet31.txt', 'TraceDataSet32.txt', 'TraceDataSet41.txt', 'TraceDataSet42.txt',
             'TraceDataSet51.txt', 'TraceDataSet52.txt']
tracedata_for_testing = ['TraceDataSet61.txt', 'TraceDataSet62.txt']
#
# PROVEDIt_sized_trace_data_mix = ['PROVEDIt_RD14-0003(021016ADG_15sec)_sized_improved1.txt', 'PROVEDIt_RD14-0003(021016ADG_15sec)_sized_improved2.txt']
# PROVEDIt_sized_trace_data_SS = ['PROVEDIt_RD14-0003(100115ADG_15sec)_sized_improved1.txt', 'PROVEDIt_RD14-0003(100115ADG_15sec)_sized_improved2.txt']
#
#
# PROVEDIt_raw_trace_data_mix = ['PROVEDIt_RD14-0003(021016ADG_15sec)_raw_improved1.txt', 'PROVEDIt_RD14-0003(021016ADG_15sec)_raw_improved2.txt']
# PROVEDIt_raw_trace_data_SS = ['PROVEDIt_RD14-0003(100115ADG_15sec)_raw_improved1.txt', 'PROVEDIt_RD14-0003(100115ADG_15sec)_raw_improved2.txt']


if __name__ == '__main__':
    # TODO: Examples of peak-labeling algorithm making mistakes
    # TODO: Apply MHCNN to our data ?

    # my_model = unet_small()
    # my_model.summary()
    # new_model = MHCNN_DT()
    # new_model.summary()

    number_of_dyes = 6
    leftoffset = 500
    rightcutoff = 4800 + 500

    train_samples = []
    for elt in tracedata_for_training:
        train_samples += rf.txt_read_sample(elt)

    test_samples = []
    for elt in tracedata_for_testing:
        test_samples += rf.txt_read_sample(elt)

    test_samples = test_samples[25:27]
    unnormalised_train, train_input, names_train = dpf.input_from_multiple_samples(train_samples, number_of_dyes, leftoffset, rightcutoff, True)
    unnormalised_test, test_input, names_test = dpf.input_from_multiple_samples(test_samples, number_of_dyes, leftoffset, rightcutoff, True)
    # Unet = trf.unet_train_test_split(train_input, test_input, 4800, "data/weights_NFI/weights_clocktime.h5", train=False,epochs=100)

    width = 80
    input_dim = 6*(width*2+1)
    DTDP_train_input = dpf.DTDP_input_from_multiple_samples(train_samples, width = width)
    DTDP_test_input = dpf.DTDP_input_from_multiple_samples(test_samples, width = width)
    FFN_model, metrics = trf.FFN(DTDP_train_input, DTDP_test_input, weightpath="data_for_github/weights_FFN_400.h5", inputsize=(input_dim,), train = False, epochs=400, batchsize=100)


    images, prediction = ppf.combine_results_FFN(DTDP_test_input, test_input, FFN_model, input_dim)
    for index_of_image in range(DTDP_test_input.data.shape[0]):
        # test_input.labels still has labels for all dyes, hence the :,0]
        pf.plot_results_FFN(images[index_of_image], prediction[index_of_image], test_input.labels[index_of_image, :, 0], "FFN_400epochs_on_"+names_test[index_of_image])

    # for sample_index in range(len(names_test)):
    #     sample = test_input.data[sample_index]
    #     truth = test_input.labels[sample_index, :, 0]
    #     result = Unet.predict(sample.reshape(1, 4800, 6))[:, :, 0].reshape(4800)
    #     s.scores(truth, result)
    # dataframe = pd.read_csv('data_for_github/FFNvUnet_scores.csv')
    # pf.scatterplot_scores_noc(dataframe)
    # pf.scatterplot_scores_mix(dataframe)
