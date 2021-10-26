from src import data_prep_functions as dpf, plotting_functions as pf, reading_functions as rf, training_functions as trf, plotting_6C_functions as pf6, write_to_csv as wf, post_processing_functions as ppf, results as r, OLD_reading_data_DTDP as rdD
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
    df = rf.read_csv_to_dataframe('FFNvUnet_scores.csv', 'data_for_github/')
    pf.boxplot_scores(df, 'mix_type', ['auc_FFN', 'auc_Unet'])
    pf.boxplot_scores(df, 'noc', ['auc_FFN', 'auc_Unet'])
    pf.boxplot_scores(df, 'mix_type', ['bin_acc_FFN', 'bin_acc_Unet'])
    pf.boxplot_scores(df, 'noc', ['bin_acc_FFN', 'bin_acc_Unet'])


    # number_of_dyes = 6
    # leftoffset = 500
    # rightcutoff = 4800 + 500
    #
    # train_samples = []
    # for elt in tracedata_for_training:
    #     train_samples += rf.txt_read_sample(elt)
    # unnormalised_train, train_input, names_train = dpf.input_from_multiple_samples(train_samples, number_of_dyes, leftoffset, rightcutoff, True)
    #
    # test_samples = []
    # for elt in tracedata_for_testing:
    #     test_samples += rf.txt_read_sample(elt)
    # unnormalised_test, test_input, names_test = dpf.input_from_multiple_samples(test_samples, number_of_dyes, leftoffset, rightcutoff, True)
    # Unet = trf.unet_train_test_split(train_input, test_input, 4800, "data/weights_NFI/weights_clocktime.h5", train=False,epochs=100)


    # width = 80
    # input_dim = 6*(width*2+1)
    # DTDP_train_input = dpf.DTDP_input_from_multiple_samples(train_samples, width = width)
    #
    # DTDP_test_input = dpf.DTDP_input_from_multiple_samples(test_samples, width = width)
    # FFN_model, metrics = trf.FFN(DTDP_train_input, DTDP_test_input, weightpath="data/weights_DTDP/weights_for_timing.h5", inputsize=(input_dim,), train = False, epochs=100, batchsize=100)
    #
    # just_the_data = DTDP_test_input.data
    # start_time_training = datetime.now()
    # for ind in range(4800):
    #     FFN_model.predict(just_the_data[ind].reshape(1,966))
    # end_time_training = datetime.now()
    # print('predicting single epg FFN: ', end_time_training-start_time_training)

    #     images, prediction = ppf.combine_results_FFN(DTDP_test_input, test_input, FFN_model, input_dim)
    # for index_of_image in range(DTDP_test_input.data.shape[0]):
    #     input = DTDP_test_input.data[index_of_image]
    #     pf.plot_results_FFN(input[:,0], prediction[:,:,0], test_input.labels[index_of_image,:,0], "Unet_fully_trained_on_"+test_sample_names[index_of_image])
    # for sample_index in range(len(names_test)):
    #     sample = test_input.data[sample_index]
    #     truth = test_input.labels[sample_index, :, 0]
    #     result = Unet.predict(sample.reshape(1,4800,6))[:,:,0].reshape(4800)
    #     pf.plot_results_FFN(sample[:,0].reshape(4800), result, truth)
    #     auc = AUC()
    #     auc.update_state(truth, result)
    #     binacc = BinaryAccuracy()
    #     binacc.update_state(truth, result)
    print('hori')
    # ax = dataframe.plot.scatter(x='auc_FFN', y = 'auc_Unet', color= 'darkviolet', marker = '*')
    # ax.plot(range(0,1,50), range(0,1,50))
    # ax.set_xlim([0.93,1])
    # ax.set_ylim([0.93,1])
    # lims = [0.93, 1]
    # # now plot both limits against eachother
    # ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
    # plt.grid()
    # ax.set_xlabel('AUC score FFN')
    # ax.set_ylabel('AUC score U-net')
    # plt.title('AUC (ROC) of U-net against FFN')
    # plt.show()
