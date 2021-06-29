from src import data_prep_functions as dpf, plotting_functions as pf, reading_functions as rf, training_functions as trf, plotting_6C_functions as pf6, post_processing_functions as ppf, results as r



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
    unet_model = trf.unet(inputs_for_unet, cutoff - leftoffset, 'data/weights_norm_avgpool.h5', False)

    donor_sets = []
    mix_types = []
    number_donors = []
    F1_scores = []
    F1_scores_corrected = []
    F1_scores_analyst = []
    new_sample_names = []
    for sample_number in range(len(sample_names)):
        sample_name, replica = sample_names[sample_number].split(".")
        # sample_data = original_sampledata[sample_number]
        input_example = inputs_for_unet.data[sample_number,:,:].reshape(1,cutoff-leftoffset,number_of_dyes,1)
        # label_example = inputs_for_unet.labels[sample_number, :, :]
        output_example = unet_model.predict(input_example).reshape(4800,6)
        actual_peaks = ppf.list_all_peaks(sample_name)
        corrected_peaks, augmented_output = ppf.check_correct_alleles_first(actual_peaks, output_example, leftoffset, 30)
        restofpeaks = ppf.mult_peaks(augmented_output, 0.5, leftoffset)
        corrected_peaks.extend(restofpeaks)
        predicted_peaks = ppf.mult_peaks(output_example, 0.5, leftoffset)
        if sample_name != "3E2":
            analyst_peaks = rf.shallow_analyst(sample_name)[int(replica)-1]
            F1_scores_analyst.append(ppf.F1_score(actual_peaks, analyst_peaks))
            F1_scores.append(ppf.F1_score(actual_peaks, predicted_peaks))
            F1_scores_corrected.append(ppf.F1_score(actual_peaks, corrected_peaks))
            new_sample_names.append(sample_names[sample_number])
            donor_set, mix_type, number_donor = sample_name
            donor_sets.append(donor_set)
            mix_types.append(mix_type)
            number_donors.append(number_donor)
    ppf.result_dataframe(new_sample_names, donor_sets, mix_types, number_donors, F1_scores, F1_scores_corrected, F1_scores_analyst)


def scores_only():
    df = rf.csv_read_scores()
    print(df.describe())

    r.make_boxplot(df, ['score', 'upper', 'analyst'])
    # r.make_boxplot(two_donors, ['score', 'upper', 'analyst'])
    # r.make_boxplot(three_donors, ['score', 'upper', 'analyst'])
    # r.make_boxplot(four_donors, ['score', 'upper', 'analyst'])
    # r.make_boxplot(five_donors, ['score', 'upper', 'analyst'])





if __name__ == '__main__':
    some_examples()
    scores_only()


