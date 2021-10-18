from src import data_prep_functions as dpf, plotting_functions as pf, reading_functions as rf, training_functions as trf, plotting_6C_functions as pf6, writing_functions as wf, post_processing_functions as ppf, results as r, reading_data_DTDP as rdD
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.metrics import BinaryAccuracy, AUC
import pandas as pd
from src import classes


tracedata_for_training = ['TraceDataSet11.txt', 'TraceDataSet12.txt', 'TraceDataSet21.txt', 'TraceDataSet22.txt',
             'TraceDataSet31.txt', 'TraceDataSet32.txt', 'TraceDataSet41.txt', 'TraceDataSet42.txt',
             'TraceDataSet51.txt', 'TraceDataSet52.txt']
tracedata_for_testing = ['TraceDataSet61.txt', 'TraceDataSet62.txt']

PROVEDIT_sized_trace_data = ['PROVEDIt_RD14-0003(010616CMG_15sec)_sized1.txt', 'PROVEDIt_RD14-0003(010616CMG_15sec)_sized2.txt', 'PROVEDIt_RD14-0003(010616CMG_15sec)_sized3.txt', 'PROVEDIt_RD14-0003(020216ADG_15sec)_sized1.txt', 'PROVEDIt_RD14-0003(020216ADG_15sec)_sized2.txt', 'PROVEDIt_RD14-0003(021716ADG_15sec)_sized1.txt', 'PROVEDIt_RD14-0003(021716ADG_15sec)_sized2.txt', 'PROVEDIt_RD14-0003(021716ADG_15sec)_sized3.txt', 'PROVEDIt_RD14-0003(022516ADG_15sec)_sized1.txt', 'PROVEDIt_RD14-0003(022516ADG_15sec)_sized2.txt', 'PROVEDIt_RD14-0003(022516ADG_15sec)_sized3.txt', 'PROVEDIt_RD14-0003(100515ADG_15sec)_sized1.txt', 'PROVEDIt_RD14-0003(100515ADG_15sec)_sized2.txt']

PROVEDIt_raw_trace_data_mix = ['PROVEDIt_RD14-0003(021016ADG_15sec)_raw1.txt', 'PROVEDIt_RD14-0003(021016ADG_15sec)_raw2.txt']
PROVEDIt_raw_trace_data_SS = ['PROVEDIt_RD14-0003(100115ADG_15sec)_raw1.txt', 'PROVEDIt_RD14-0003(100115ADG_15sec)_raw2.txt']

#
if __name__ == '__main__':
    # number_of_dyes = 6
    # test_samples = []
    # for elt in tracedata_for_testing:
    #     test_samples += rf.txt_read_sample(elt)
    #
    # leftoffset = 500
    # rightcutoff = 4800 + 500
    # #
    # unnormalised, test_input, names = dpf.input_from_multiple_samples(test_samples, number_of_dyes, leftoffset, rightcutoff, True)
    # Unet = trf.unet_train_test_split([], test_input, 4800, "data/weights_NFI/weights_6_split_300epochs+LRs100.h5", train=False,epochs=100)

    # PROVEDIt_samples = []
    # for elt in PROVEDIT_sized_trace_data:
    #     PROVEDIt_samples += rf.txt_read_sized_sample_PROVEDIt(elt)
    # originals, PROVEDIt_input, names = dpf.input_from_multiple_PROVEDIt_samples(PROVEDIt_samples, number_of_dyes, leftoffset, rightcutoff, True)
    # Unet = trf.unet_train_test_split([], PROVEDIt_input, rightcutoff-leftoffset, "data/weights_NFI/weights_6_split_300epochs+LRs100.h5", train=False)
    #

    # width = 80
    # input_dim = 6*(width*2+1)
    # DTDP_test_input = dpf.DTDP_input_from_multiple_samples(test_samples, width = width)
    # score_binacc = []
    # score_auc = []
    # for name_index in range(len(names)):
    #     newtestinput = classes.DTDPTrainInput([], DTDP_test_input.data[4800*name_index:4800*name_index+4800], DTDP_test_input.labels[4800*name_index:4800*name_index+4800])
    #     FFN_model, metrics = trf.FFN([], newtestinput, weightpath="data/weights_DTDP/weights_FFN_our_data_w80_100epochs.h5", inputsize=(input_dim,), train = False, epochs=100, batchsize=100)
    #     loss, binacc, auc = metrics
    #     score_binacc.append(binacc)
    #     score_auc.append(auc)
    # datadict = {'name': names, 'bin_acc': score_binacc, 'auc': score_auc}
    # dataframe = pd.DataFrame(datadict)
    # dataframe.to_csv('data/results_paper/FFN_blue_dye.csv')

    # images, prediction = ppf.combine_results_FFN(DTDP_test_input, test_input, FFN_model, input_dim)
    # for index_of_image in range(DTDP_test_input.data.shape[0]):
    #     input = DTDP_test_input.data[index_of_image]
    #     pf.plot_results_FFN(input[:,0], prediction[:,:,0], test_input.labels[index_of_image,:,0], "Unet_fully_trained_on_"+test_sample_names[index_of_image])
    # for sample_index in range(len(names)):
    #     sample = test_input.data[sample_index]
    #     truth = test_input.labels[sample_index, :, 0]
    #     result = Unet.predict(sample.reshape(1,4800,6))[:,:,0].reshape(4800)
    #     auc = AUC()
    #     auc.update_state(truth, result)
    #     binacc = BinaryAccuracy()
    #     binacc.update_state(truth, result)
    # dataframe = pd.read_csv('data/results_paper/FFNvUnet_bluedye.csv')
    # ax = dataframe.plot.scatter(x='auc_FFN', y = 'auc_Unet', color= 'darkviolet', marker = '*')
    # ax.set_xlim([0.93,1])
    # ax.set_ylim([0.93,1])
    # plt.grid()
    # ax.set_xlabel('AUC score FFN')
    # ax.set_ylabel('AUC score U-net')
    # plt.title('AUC (ROC) of U-net against FFN')
    # plt.show()
