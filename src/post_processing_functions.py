from src.classes import *
import numpy as np
from src import reading_functions as rf


def mult_peaks(unet_output: np.ndarray, threshold: float, left_offset: int):
    result = unet_output > threshold
    allele_list = []
    for dye in range(result.shape[1]-1):
        # -1 so we don't iterate over size std
        current = result[:, dye]
        index_start = 0
        while index_start != len(current) - 1:
            alleles = {}
            # find next True
            while current[index_start] == False and index_start < len(current) - 1:
                index_start += 1
            index_end = index_start
            # find corresponding end True
            while current[index_end] == True and index_end < len(current) - 1:
                allele = allele_map[index_end+left_offset, dye]
                prob = unet_output[index_end,dye]
                if allele in alleles:
                    alleles[allele] *= prob
                else:
                    alleles[allele] = prob
                index_end += 1

            if index_end - index_start < 5:
                index_start = index_end
            else:
                alleles[None] = 0
                decision = max(alleles.items(), key=lambda x: x[1])
                allele_list.append(decision[0])
                # TODO: may need probabilities later
                index_start = index_end
    return allele_list


def check_correct_alleles_first(alleles_present: List, unet_output: np.ndarray, left_offset: int, halfpeakwidth: int):
    unet_output_augmented = unet_output.copy()
    alleles_detected = []
    for locus_allele in alleles_present:
        locus_name, allele_name = locus_allele.split("_")
        allele = locus_dict[locus_name].alleles[allele_name]
        dye_index = allele.dye.plot_index - 1
        index_left = round((allele.mid-allele.left)*10) - left_offset
        index_right = round((allele.mid+allele.right)*10) - left_offset
        prob = sum(unet_output[index_left-halfpeakwidth:index_right+halfpeakwidth, dye_index])/(index_right-index_left)
        if prob > 0.5:
            alleles_detected.append(locus_allele)
            unet_output_augmented[index_left-halfpeakwidth:index_right+halfpeakwidth, dye_index] = 0
    return alleles_detected, unet_output_augmented


def list_all_peaks(mix_name: str):
    person_mix = rf.make_person_mixture(mix_name)
    peak_list = []
    # iterate through persons in mix
    for person in person_mix.persons:
        # iterate over their alleles
        for locus_allele in person.alleles:
            if locus_allele not in peak_list:
                peak_list.append(locus_allele)
    return peak_list


def F1_score(alleles_present: List, alleles_detected: List):
    """Calculates F1-score of result of U-net"""
    positives = set(alleles_detected)
    truth = set(alleles_present)
    TP = len(positives & truth)
    FP = len(positives - truth)
    FN = len(truth - positives)
    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    return 2*(precision*recall)/(precision+recall)


def combine_results_FFN(testset: DTDPTrainInput, testset_full_images: TrainInput, model, input_length: int):
    images = testset_full_images.data[:,:,0]  # only blue
    labels = []
    for image_index in range(images.shape[0]):
        prediction_array = np.zeros(4800)
        for point in range(4800):
            prediction = model.predict(testset.data[image_index*4800 + point].reshape(1, input_length))
            prediction_array[point] = prediction
        labels.append(prediction_array)
    return images, np.array(labels)

