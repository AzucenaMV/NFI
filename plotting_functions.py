import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from classes import *


def plot_sample_markers(sample: Sample, locus_dict: dict):
    """Plots sample and markers in 6C plot"""
    fig = plt.figure()
    # iterate through all loci to plot markers
    for key_locus in locus_dict:
        locus = locus_dict[key_locus]               # get locus class object
        plt.subplot(6, 1, locus.dye.plot_index)     # plot in correct color location
        # plot bar at level 0 with squares as endpoints to show marker
        # might want to change style of endpoints
        plt.annotate(s='', xy=(locus.lower,0), xytext=(locus.upper, 0), arrowprops=dict(arrowstyle='<->'))
        # plt.plot([locus.lower, locus.upper], [0, 0], color = locus.dye.plot_color, marker = "s")
    for i in range(6):
        plt.subplot(6, 1, i + 1)
        current = sample.data[:, i]
        plt.plot(np.linspace(0, len(current)/10, len(current)), current, str(sample.color_list[i].plot_color))
        plt.xlim([50,500])
    plt.suptitle(sample.name)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()

### UNDERNEATH ARE MOSTLY UNUSED ###
def plot_data(sample: Sample):
    """"Simple plot of all colors of one sample in the same figure"""
    plt.figure()
    for i in range(6):
        plt.plot(sample.data[:, i], label=str(sample.color_list[i]))
    plt.legend()
    plt.title(sample.name)
    plt.show()
    return None


def plot_6C(sample: Sample):
    """"Plots one combined plot of all 6 colors of one sample"""
    plt.figure()
    plt.suptitle(sample.name)
    for i in range(6):
        plt.subplot(6, 1, i + 1)
        plt.plot(sample.data[:, i])
        plt.title(sample.color_list[i])
    plt.show()
    return None


def plot_analyst(peaks: list, sample: Sample):
    """uses both the analysts identified peaks and sized data \
    for comparison to plot both in one image for each color"""
    for j in range(6):
        plt.figure()
        plt.title(str('filename: '+sample.name+', dye: ' + str(sample.color_list[j])))
        plt.xlim([50, 500])     # to cut off primer dimer
        current_plot = sample.data[:, j]
        # plot measured data
        plt.plot(np.linspace(0, len(current_plot)/10, len(current_plot)), current_plot)
        # to scale y-axis somewhat close to data
        plt.ylim([-50, max(current_plot[1000:])*1.5])
        # iterate through all alleles in mixture
        for peak in peaks:
            dye = peak.dye
            dye_name = dye.name
            color = dye.plot_color
            # this is not very efficient
            # iterates entire mixture every time, then checks the color
            # does 6 times as much work as needed...
            if dye_name == sample.color_list[j]:
                plt.plot([peak.x], [peak.height], str(color + "*"))  # add colour
        plt.show()
    pass


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


def plot_expected(peaks: list, sample: Sample):
    """uses both the theoretical actual relative peaks and \
    sized data for comparison to plot both in one image"""

    for j in range(6):
        # makes one separate figure per dye
        plt.figure()
        plt.title(str('filename: '+sample.name+', dye: ' + str(sample.color_list[j])))
        current_plot = sample.data[:, j]
        # cut off primer dimer
        plt.xlim([50, 500])
        # amount to multiply relative peak height with
        max_rel = 20000
        # set y_max at 1.5 times max peak
        plt.ylim([-50, max(max(current_plot[1000:]) * 1.5, max_rel)])
        # plot max height relative points
        plt.hlines(max_rel, 0, 500)
        # plot measured data
        plt.plot(np.linspace(0, len(current_plot)/10, len(current_plot)), current_plot)
        # iterate through dict to plot all peaks as *
        for peak in peaks:
            dye = peak.dye
            if dye.name == sample.color_list[j]:
                color = dye.plot_color
                plt.plot([peak.x], [peak.height * max_rel], str(color + "*"))  # add colour
        plt.show()
    pass


def plot_markers(locusDict):
    """Just a quick function to test marker boundaries"""
    plt.figure()
    # iterate through all loci
    for key_locus in locusDict:
        locus = locusDict[key_locus]            # get locus class object
        plt.subplot(6, 1, locus.dye.plot_index)     # plot in correct color location
        # plot bar at level 0 with squares as endpoints to show marker
        plt.plot([locus.lower, locus.upper], [0, 0], color = locus.dye.plot_color, marker = "s")
        # iterate through all alleles
        for key_allele in locus.alleles:
            allele = locus.alleles[key_allele]  # get allele class object
            start = allele.mid - allele.left    # calculate where it starts
            end = allele.mid + allele.right     # calculate where it ends
            plt.plot([start, end], [1, 1])       # plot allele bin at level 1
    plt.show()
