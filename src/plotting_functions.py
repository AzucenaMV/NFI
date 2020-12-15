import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from src.classes import *
import matplotlib.collections as collections


def initialise_figure(fig_size = (15,5)):
    fig, ax = plt.subplots(figsize = fig_size)
    plt.xlim([50,500])
    return fig, ax


def initialise_6C_figure(fig_size = (20,30)):
    fig, axes = plt.subplots(nrows = 6, figsize = fig_size)
    plt.xlim([50,500])
    return fig, axes


def plot_sample_array(sample_array, plot_color = "k"):
    plt.plot(np.linspace(0, len(sample_array) / 10, len(sample_array)), sample_array, plot_color)
    plt.ylim([0, max(sample_array[1000:]) * 1.2])


def plot_locus_bins(dye_color: Dye):
    # make dict of loci present in chosen dye
    loci_on_dye = {locus_name: locus for (locus_name, locus) in locus_dict.items() if locus.dye == dye_color}
    for (locus_name, locus) in loci_on_dye.items():
        plt.annotate(text="", xy=(locus.lower, 0), xytext=(locus.upper, 0), arrowprops=dict(arrowstyle='<->'))


def plot_peaks_analyst(peak_list: list, dye_color: Dye):
    for peak in peak_list:
        dye = peak.allele.dye
        if dye == dye_color:
            plt.plot([peak.allele.mid], [peak.height], str(dye.plot_color + "*"))


def plot_peaks_expected(peak_list: list, max_rel, dye_color: Dye):
    # amount to multiply relative peak height with
    plt.ylim([-50, max_rel])
    # plot max height relative points
    plt.hlines(max_rel, 0, 500)
    for peak in peak_list:
        dye = peak.allele.dye
        if dye == dye_color:
            color = dye.plot_color
            plt.plot([peak.allele.mid], [peak.height * max_rel], str(color + "*"))


def finish_plot(show_or_title = "show"):
    if show_or_title == "show":
        plt.show()
    else:
        plt.savefig(show_or_title+".png")
        plt.close()


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


def plot_analyst(peaks: list, sample: Sample):
    """uses both the analysts identified peaks and sized data \
    for comparison to plot both in one image for each color"""
    for j in range(6):
        current_plot = sample.data[:, j]
        current_dye = Dyes.color_list[j]
        initialise_figure()
        # plt.title(str('filename: '+sample.name+', dye: ' + str(Dyes.color_list[j].name)))
        plot_sample_array(current_plot)
        plot_locus_bins(current_dye)
        plot_peaks_analyst(peaks, current_dye)
        title = "Sample_"+sample.name+"_"+str(sample.replica)+"_analyst_peaks_"+current_dye.name
        finish_plot()


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
    # plt.suptitle(sample.name)       # set title
    plt.tight_layout()  # ensures subplots don't overlap
    plt.subplots_adjust(top=0.9)  # ensures title doesn't overlap plots
    plt.show()


def plot_expected(peaks: list, sample: Sample):
    """uses both the theoretical actual relative peaks and \
    sized data for comparison to plot both in one image"""
    for j in range(6):
        # makes one separate figure per dye
        initialise_figure()
        # plt.title(str('filename: '+sample.name+', dye: ' + Dyes.color_list[j].name))
        current_plot = sample.data[:, j]
        current_dye = Dyes.color_list[j]
        max_relative = max(current_plot[1000:]) * 1.5
        plt.hlines(max_relative, 0, 500)
        plot_sample_array(current_plot)
        plot_peaks_expected(peaks, max_relative, current_dye)
        plot_locus_bins(current_dye)
        finish_plot()  # "Sample_"+sample.name+"_"+str(sample.replica)+"_expected_peaks_"+current_dye.name)


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
        plt.annotate(text="", xy=(locus.lower, 0), xytext=(locus.upper, 0), arrowprops=dict(arrowstyle='<->'))
    # plt.suptitle(sample.name)       # set title
    plt.tight_layout()  # ensures subplots don't overlap
    plt.subplots_adjust(top=0.9)  # ensures title doesn't overlap plots
    plt.show()


# ## UNDERNEATH ARE MOSTLY UNUSED ###
def plot_sizestd_peaks(sizestd):
    """The goal of this function was to determine the factor needed \
    for resizing the sized data to base pairs\
    Input is one size standard array, output was a plot"""
    peaks, rest = find_peaks(sizestd, distance=200)
    plt.figure()
    plt.plot(sizestd)
    print(peaks)
    plt.plot(peaks, sizestd[peaks], "*")
    plt.show()
    return peaks


def plot_markers():
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


def plot_labeled_sample(blue_data, peak_bools):
    peaks = [blue_data[i] if peak_bools[i] else 0 for i in range(len(blue_data))]
    not_peaks = blue_data - peaks
    initialise_figure(fig_size=(30,5))
    plot_sample_array(not_peaks, 'r')
    plot_sample_array(peaks, 'b')
    plot_locus_bins(Dyes.BLUE)
    plt.show()


def plot_background(sample_array, peak_bools):
    # note that sample_array and peak_bools have the same shape
    fig, ax = initialise_figure(fig_size = (30,5))
    plot_sample_array(sample_array)
    x = np.linspace(0, len(sample_array) / 10, len(sample_array))
    # plot background of peaks in green
    collection = collections.BrokenBarHCollection.span_where(x, ymin=0, ymax=max(sample_array), where=peak_bools, facecolor='green', alpha=0.5)
    ax.add_collection(collection)
    # plot non-peaks in red
    collection = collections.BrokenBarHCollection.span_where(x, ymin=0, ymax=max(sample_array), where=~peak_bools, facecolor='red', alpha=0.5)
    ax.add_collection(collection)
    plot_locus_bins(Dyes.BLUE)
    plt.show()
