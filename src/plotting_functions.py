import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from src.classes import *


def plot_sample_markers_6C(sample: Sample, locus_dict: dict):
    """Plots sample and markers in 6C plot"""
    plt.figure() #figsize = (10,10))
    # iterate through all loci to plot markers
    for key_locus in locus_dict:
        locus = locus_dict[key_locus]               # get locus class object
        plt.subplot(6, 1, locus.dye.plot_index)     # plot in correct color location
        plt.annotate(text="", xy=(locus.lower, 0), xytext=(locus.upper, 0), arrowprops=dict(arrowstyle='<->'))
    for i in range(6):
        plt.subplot(6, 1, i + 1)
        current = sample.data[:, i]
        plt.plot(np.linspace(0, len(current)/10, len(current)), current, str(Dyes.color_list[i].plot_color))
        plt.xlim([50, 500])
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()


def plot_analyst(peaks: list, sample: Sample, locus_dict):
    """uses both the analysts identified peaks and sized data \
    for comparison to plot both in one image for each color"""
    for j in range(6):
        plt.figure()
        #plt.title(str('filename: '+sample.name+', dye: ' + str(Dyes.color_list[j].name)))
        plt.xlim([50, 500])     # to cut off primer dimer
        current_plot = sample.data[:, j]
        # plot measured data
        plt.plot(np.linspace(0, len(current_plot)/10, len(current_plot)), current_plot)
        # to scale y-axis somewhat close to data
        plt.ylim([-50, max(current_plot[1000:])*1.5])
        # iterate through all alleles in mixture
        for peak in peaks:
            dye = peak.allele.dye
            if dye.plot_index == j + 1:
                plt.plot([peak.allele.mid], [peak.height], str(dye.plot_color + "*"))
        for locus_key in locus_dict:
            locus = locus_dict[locus_key]
            if locus.dye.plot_index == j + 1:
                plt.annotate(text='', xy=(locus.lower, 0), xytext=(locus.upper, 0), arrowprops=dict(arrowstyle='<->'))
        plt.show()


def plot_analyst_6C(peaks: list, sample: Sample, locus_dict):
    """uses both the analysts identified peaks and sized data \
    for comparison to plot both in one image for each color"""
    plt.figure()
    for j in range(6):
        plt.subplot(6, 1, j + 1)
        plt.xlim([50, 500])     # to cut off primer dimer
        current_plot = sample.data[:, j]
        # plot measured data
        plt.plot(np.linspace(0, len(current_plot)/10, len(current_plot)), current_plot, Dyes.color_list[j].plot_color)
        # to scale y-axis somewhat close to data
        plt.ylim([-50, max(current_plot[1000:])*1.5])
        # iterate through all alleles in mixture
    for peak in peaks:
        dye = peak.allele.dye
        plt.subplot(6, 1, dye.plot_index)
        plt.plot([peak.allele.mid], [peak.height], "k*")
    for key_locus in locus_dict:
        locus = locus_dict[key_locus]               # get locus class object
        plt.subplot(6, 1, locus.dye.plot_index)     # plot in correct color location
        plt.annotate(text="", xy=(locus.lower, 0), xytext=(locus.upper, 0), arrowprops=dict(arrowstyle='<->'))
    #plt.suptitle(sample.name)       # set title
    plt.tight_layout()              # ensures subplots don't overlap
    plt.subplots_adjust(top=0.9)    # ensures title doesn't overlap plots
    plt.show()


def plot_expected(peaks: list, sample: Sample, locus_dict: dict):
    """uses both the theoretical actual relative peaks and \
    sized data for comparison to plot both in one image"""

    for j in range(6):
        # makes one separate figure per dye
        plt.figure()
        #plt.title(str('filename: '+sample.name+', dye: ' + Dyes.color_list[j].name))
        current_plot = sample.data[:, j]
        # cut off primer dimer
        plt.xlim([50, 500])
        # amount to multiply relative peak height with
        max_rel = max(current_plot[1000:]) * 1.5
        # set y_max at 1.5 times max peak
        plt.ylim([-50, max_rel])
        # plot max height relative points
        plt.hlines(max_rel, 0, 500)
        # plot measured data
        plt.plot(np.linspace(0, len(current_plot)/10, len(current_plot)), current_plot)
        # iterate through dict to plot all peaks as *
        for peak in peaks:
            dye = peak.allele.dye
            if dye.plot_index == j + 1:
                color = dye.plot_color
                plt.plot([peak.allele.mid], [peak.height * max_rel], str(color + "*"))  # add colour
        for locus in locus_dict:
            if locus.dye.plot_index == j + 1:
                plt.annotate(text='', xy=(locus.lower, 0), xytext=(locus.upper, 0), arrowprops=dict(arrowstyle='<->'))
        plt.show()


def plot_expected_6C(peaks: list, sample: Sample, locus_dict):
    """uses both the analysts identified peaks and sized data \
    for comparison to plot both in one image for each color"""
    max_rel_list = []
    plt.figure()
    for j in range(6):
        plt.subplot(6, 1, j + 1)
        plt.xlim([50, 500])     # to cut off primer dimer
        current_plot = sample.data[:, j]
        # amount to multiply relative peak height with
        max_rel = max(current_plot[1000:]) * 1.5
        max_rel_list.append(max_rel)
        # set y_max at 1.5 times max peak
        plt.ylim([-50, max_rel])
        # plot max height relative points
        plt.hlines(max_rel, 0, 500)
        # plot measured data
        plt.plot(np.linspace(0, len(current_plot)/10, len(current_plot)), current_plot, Dyes.color_list[j].plot_color)
    # iterate through all peaks in mixture
    for peak in peaks:
        dye = peak.allele.dye
        plt.subplot(6, 1, dye.plot_index)
        plt.plot([peak.allele.mid], [peak.height * max_rel_list[dye.plot_index-1]], "k*")  # add black colour
    for key_locus in locus_dict:
        locus = locus_dict[key_locus]               # get locus class object
        plt.subplot(6, 1, locus.dye.plot_index)     # plot in correct color location
        plt.annotate(text="", xy=(locus.lower, 0), xytext=(locus.upper, 0), arrowprops=dict(arrowstyle='<->'))
    #plt.suptitle(sample.name)       # set title
    plt.tight_layout()              # ensures subplots don't overlap
    plt.subplots_adjust(top=0.9)    # ensures title doesn't overlap plots
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


def plot_markers(locus_dict):
    """Just a quick function to test marker boundaries"""
    plt.figure()
    # iterate through all loci
    for key_locus in locus_dict:
        locus = locus_dict[key_locus]            # get locus class object
        plt.subplot(6, 1, locus.dye.plot_index)     # plot in correct color location
        # plot bar at level 0 with squares as endpoints to show marker
        plt.plot([locus.lower, locus.upper], [0, 0], color=locus.dye.plot_color, marker="s")
        # iterate through all alleles
        end = 0
        for key_allele in locus.alleles:
            allele = locus.alleles[key_allele]  # get allele class object
            start = allele.mid - allele.left    # calculate where it starts
            if start < end:
                print(key_locus+": "+key_allele+" starts at "+str(start)+", previous ends at "+str(end))
            end = allele.mid + allele.right     # calculate where it ends
            plt.plot([start, end], [1, 1])      # plot allele bin at level 1
    plt.show()
