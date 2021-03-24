import numpy
from matplotlib import pyplot as plt
from src.classes import *


def initialise_6C_figure(fig_size=(20, 30)):
    fig, axes = plt.subplots(nrows=6, figsize=fig_size)
    plt.xlim([50, 500])
    return fig, axes


def plot_results_unet(input, result, fig_size = (20,30)):
    fig, axes = plt.subplots(nrows=6, figsize=fig_size)
    input = input.squeeze()
    result = result.squeeze()
    number_of_dyes = result.shape[1]
    for dye in range(number_of_dyes):
        axes[dye].plot(30000*result[:,dye])
        axes[dye].plot(input[:, dye])
    fig.show()
    fig.close()


def plot_sample_markers_6C(sample: Sample):
    """Plots sample and markers in 6C plot"""
    plt.figure()
    # iterate through all loci to plot markers
    for key_locus in locus_dict:
        locus = locus_dict[key_locus]  # get locus class object
        plt.subplot(6, 1, locus.dye.plot_index)  # plot in correct color location
        plt.annotate(text="", xy=(locus.lower, 0), xytext=(locus.upper, 0), arrowprops=dict(arrowstyle='<->'))
    for i in range(6):
        plt.subplot(6, 1, i + 1)
        current = sample.data[:, i]
        plt.plot(np.linspace(0, len(current) / 10, len(current)), current, str(Dyes.color_list[i].plot_color))
        plt.xlim([50, 500])
        plt.ylim(0, max)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()


def plot_analyst_6C(peaks: list, sample: Sample):
    """uses both the analysts identified peaks and sized data \
    for comparison to plot both in one image for each color"""
    plt.figure()
    for j in range(6):
        plt.subplot(6, 1, j + 1)
        plt.xlim([50, 500])  # to cut off primer dimer
        current_plot = sample.data[:, j]
        # plot measured data
        plt.plot(np.linspace(0, len(current_plot) / 10, len(current_plot)), current_plot, Dyes.color_list[j].plot_color)
        # to scale y-axis somewhat close to data
        plt.ylim([-50, max(current_plot[1000:]) * 1.5])
        # iterate through all alleles in mixture
    for peak in peaks:
        dye = peak.allele.dye
        plt.subplot(6, 1, dye.plot_index)
        plt.plot([peak.allele.mid], [peak.height], "k*")
    for key_locus in locus_dict:
        locus = locus_dict[key_locus]  # get locus class object
        plt.subplot(6, 1, locus.dye.plot_index)  # plot in correct color location
        plt.annotate(text="", xy=(locus.lower, 0), xytext=(locus.upper, 0), arrowprops=dict(arrowstyle='<->'))
    plt.tight_layout()  # ensures subplots don't overlap
    plt.subplots_adjust(top=0.9)  # ensures title doesn't overlap plots
    plt.show()


def plot_expected_6C(peaks: list, sample: Sample):
    """uses both the analysts identified peaks and sized data \
    for comparison to plot both in one image for each color"""
    max_rel_list = []
    plt.figure()
    for j in range(6):
        plt.subplot(6, 1, j + 1)
        plt.xlim([50, 500])  # to cut off primer dimer
        current_plot = sample.data[:, j]
        # amount to multiply relative peak height with
        max_rel = max(current_plot[1000:]) * 1.5
        max_rel_list.append(max_rel)
        # set y_max at 1.5 times max peak
        plt.ylim([-50, max_rel])
        # plot max height relative points
        plt.hlines(max_rel, 0, 500)
        # plot measured data
        plt.plot(np.linspace(0, len(current_plot) / 10, len(current_plot)), current_plot, Dyes.color_list[j].plot_color)
    # iterate through all peaks in mixture
    for peak in peaks:
        dye = peak.allele.dye
        plt.subplot(6, 1, dye.plot_index)
        plt.plot([peak.allele.mid], [peak.height * max_rel_list[dye.plot_index - 1]], "k*")  # add black colour
    for key_locus in locus_dict:
        locus = locus_dict[key_locus]  # get locus class object
        plt.subplot(6, 1, locus.dye.plot_index)  # plot in correct color location
        plt.annotate(text="", xy=(locus.lower, 0), xytext=(locus.upper, 0),
                     arrowprops=dict(color='b', arrowstyle='<->'))
    plt.tight_layout()  # ensures subplots don't overlap
    plt.subplots_adjust(top=0.9)  # ensures title doesn't overlap plots
    plt.show()


def plot_all_markers_and_bins():
    """Just a quick function to test marker boundaries"""
    plt.figure()
    # iterate through all loci
    for key_locus in locus_dict:
        locus = locus_dict[key_locus]  # get locus class object
        plt.subplot(6, 1, locus.dye.plot_index)  # plot in correct color location
        # plot bar at level 0 with squares as endpoints to show marker
        plt.plot([locus.lower, locus.upper], [0, 0], color=locus.dye.plot_color, marker="s")
        # iterate through all alleles
        end = 0
        for key_allele in locus.alleles:
            allele = locus.alleles[key_allele]  # get allele class object
            start = allele.mid - allele.left  # calculate where it starts
            end = allele.mid + allele.right  # calculate where it ends
            plt.plot([start, end], [1, 1])  # plot allele bin at level 1
    plt.show()
    plt.close()
