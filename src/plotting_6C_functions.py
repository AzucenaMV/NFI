from matplotlib import pyplot as plt
from src.classes import *
import matplotlib.collections as collections
from sklearn.preprocessing import normalize


def plot_inputs_PROVEDIt(result: np.array, title: str, leftoffset=50, fig_size=(25, 15)):
    # wanted to check out the data without labels
    number_of_dyes = 6
    fig, axes = plt.subplots(nrows=number_of_dyes, figsize=fig_size)
    result = result.squeeze()
    x_array = np.linspace(0, len(result) / 10, len(result))
    for dye in range(number_of_dyes):
        y_max = 1
        y_min = -0.1 * y_max  # always a 10% gap on bottom for legibility
        axes[dye].set_ylim([y_min, y_max])
        plot_markers(Dyes.color_list[dye], axes[dye], locus_dict_alt, y_min, leftoffset)
        axes[dye].plot(x_array, result[:, dye], "k")
        axes[dye].set_xlim([0, 480])
    plt.title(title)
    plt.show()
    plt.close()


def plot_results_unet_against_truth(input, result, label, title=False, leftoffset=50, fig_size=(30, 20)):
    number_of_dyes = 6
    fig, axes = plt.subplots(nrows=number_of_dyes, figsize=fig_size)
    input = input.squeeze()
    result = result.squeeze()
    x_array = np.linspace(0, len(result) / 10, len(result))
    for dye in range(number_of_dyes):
        y_max = 1  # min(1000, 0.1 * max(input[:,dye]))
        y_min = -0.1 * y_max  # always a 10% gap on bottom for legibility
        axes[dye].set_xlim([0, 480])
        axes[dye].set_ylim([y_min, y_max])
        plot_markers(Dyes.color_list[dye], axes[dye], locus_dict_alt, y_min, leftoffset)
        axes[dye].plot(x_array, input[:, dye], "k")
        axes[dye].axhline(y=500, linestyle="--", color="gray")
        # plot result
        line1, = axes[dye].plot(x_array, y_max * result[:, dye], color="magenta")
        # plot truth
        plot_labels(input[:, dye], label[:, dye], axes[dye], y_min, y_max, alph=0.3, nopeak="w", peak="c")
        ax_right = axes[dye].twinx()
        ax_right.set_ylim([-0.1, 1])
        ax_right.spines["right"].set_color(line1.get_color())
        ax_right.tick_params(axis='y', colors=line1.get_color())
    if not title:
        plt.show()
    else:
        plt.savefig(str(title) + ".png")
    plt.close()


def plot_results_unet_against_truth_alt(input, result, label, title=False, leftoffset=50, fig_size=(30, 20)):
    number_of_dyes = 6
    fig, axes = plt.subplots(nrows=number_of_dyes, figsize=fig_size)
    input = input.squeeze()
    result = result.squeeze()
    x_array = np.linspace(0, len(result) / 10, len(result))
    for dye in range(number_of_dyes):
        y_max = 1000  # min(1000, 0.1 * max(input[:,dye]))
        y_min = -0.1 * y_max  # always a 10% gap on bottom for legibility
        axes[dye].set_xlim([0, 480])
        axes[dye].set_ylim([y_min, y_max])
        plot_markers(Dyes.color_list[dye], axes[dye], y_min, leftoffset)
        axes[dye].plot(x_array, input[:, dye], "k")
        # plot result
        line1, = axes[dye].plot(x_array, y_max * result[:, dye])
        # plot truth
        collection = collections.BrokenBarHCollection.span_where(x_array, ymin=y_min, ymax=y_max,
                                                                 where=label[:, dye],
                                                                 facecolor='green', alpha=0.5)
        axes[dye].add_collection(collection)
        # plot result
        collection = collections.BrokenBarHCollection.span_where(x_array, ymin=y_min, ymax=y_max,
                                                                 where=(result > 0.5)[:, dye],
                                                                 facecolor='blue', alpha=0.3)
        axes[dye].add_collection(collection)
        ax_right = axes[dye].twinx()
        ax_right.set_ylim([-0.1, 1])
        ax_right.spines["right"].set_color(line1.get_color())
        ax_right.tick_params(axis='y', colors=line1.get_color())
    if not title:
        plt.show()
    else:
        plt.savefig(str(title) + ".png")
    plt.close()


def plot_inputs_unet(input, label, leftoffset=50, fig_size=(30, 20), rescale=10):
    number_of_dyes = 6
    fig, axes = plt.subplots(nrows=number_of_dyes, figsize=fig_size)
    input = input.squeeze()
    x_array = np.linspace(0, len(input) / rescale, len(input))
    for dye in range(number_of_dyes):
        y_max = 1000  # min(1000, 0.1 * max(input[:,dye]))
        y_min = -0.1 * y_max  # always a 10% gap on bottom for legibility
        # axes[dye].set_ylim([y_min, y_max])
        plot_markers(Dyes.color_list[dye], axes[dye], y_min, leftoffset)
        axes[dye].plot(x_array, input[:, dye], "k")
        # axes[dye].set_xlim([0,480])
        # plot truth
        plot_labels(input[:, dye], label[:, dye], axes[dye], y_min, y_max, rescale=rescale)
    plt.show()
    plt.close()


def plot_labels(sample_array, peak_bools, ax, y_min, y_max, alph=0.5, nopeak="purple", peak="green", rescale=10):
    # note that sample_array and peak_bools have the same shape
    x = np.linspace(0, len(sample_array) / rescale, len(sample_array))
    # plot background of peaks in green
    collection = collections.BrokenBarHCollection.span_where(x, ymin=y_min, ymax=y_max, where=peak_bools,
                                                             facecolor=peak, alpha=alph)
    ax.add_collection(collection)
    # plot background of non-peaks in red
    collection = collections.BrokenBarHCollection.span_where(x, ymin=y_min, ymax=y_max, where=~peak_bools,
                                                             facecolor=nopeak, alpha=alph)
    ax.add_collection(collection)


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
        plt.ylim(0, 2000)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()


def plot_markers(dye_color: Dye, ax, dyekit: {}, vertical=0.0, leftoffset=50):
    # make dict of loci present in chosen dye
    loci_on_dye = {locus_name: locus for (locus_name, locus) in dyekit.items() if locus.dye == dye_color}
    newticklist = []
    newlabellist = []
    for (locus_name, locus) in loci_on_dye.items():
        ax.annotate(text="", xy=(locus.lower - leftoffset, vertical), xytext=(locus.upper - leftoffset, vertical),
                    arrowprops=dict(arrowstyle='<->', color='b'))
        newticklist.append((locus.lower + locus.upper) / 2 - leftoffset)
        newlabellist.append(locus_name)
    ax.set_xticks(newticklist)
    ax.set_xticklabels(newlabellist)


def OLD_plot_analyst_6C(peaks: list, sample: Sample):
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


def OLD_plot_expected_6C(peaks: list, sample: Sample):
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


def choose_normalisation(original, leftoffset=50, fig_size=(15, 10)):
    """Visualising some options to choose a normalisation from"""
    number_of_dyes = 6
    original = original.squeeze()

    minima = [min(original[:, i]) for i in range(number_of_dyes)]
    norm_per_dye = normalize(original - minima, axis=0, norm="max")

    minimised = original - np.min(original)
    norm_per_image = minimised / np.max(minimised)

    x_array = np.linspace(0, len(original) / 10, len(original))

    # norm1
    fig, axes = plt.subplots(nrows=number_of_dyes, figsize=fig_size)
    y_min = np.min(original)
    y_max = np.max(original)
    for dye in range(number_of_dyes):
        plot_markers(Dyes.color_list[dye], axes[dye], 0, leftoffset)
        axes[dye].plot(x_array, original[:, dye], "k")
        axes[dye].set_ylim([y_min, y_max])
    fig.suptitle("original")
    plt.show()
    plt.close()

    # norm2
    fig, axes = plt.subplots(nrows=number_of_dyes, figsize=fig_size)
    for dye in range(number_of_dyes):
        plot_markers(Dyes.color_list[dye], axes[dye], 0, leftoffset)
        axes[dye].plot(x_array, norm_per_dye[:, dye], "k")
        axes[dye].set_ylim([0, 1])
    fig.suptitle("per dye")
    plt.show()
    plt.close()

    # norm3
    fig, axes = plt.subplots(nrows=number_of_dyes, figsize=fig_size)
    for dye in range(number_of_dyes):
        plot_markers(Dyes.color_list[dye], axes[dye], 0, leftoffset)
        axes[dye].plot(x_array, norm_per_image[:, dye], "k")
        axes[dye].set_ylim([0, 1])
    fig.suptitle("per image")
    plt.show()
    plt.close()

    # norm4
    fig, axes = plt.subplots(nrows=number_of_dyes, figsize=fig_size)
    for dye in range(number_of_dyes):
        plot_markers(Dyes.color_list[dye], axes[dye], 0, leftoffset)
        axes[dye].plot(x_array, norm_per_image[:, dye], "k")
        axes[dye].set_ylim([0, 1])
    fig.suptitle("per image")
    plt.show()
    plt.close()


def plot_bins_vs_labels(input, labels_peaks, labels_bins, title=False, leftoffset=50, fig_size=(30, 20)):
    number_of_dyes = 6
    fig, axes = plt.subplots(nrows=number_of_dyes, figsize=fig_size)
    input = input.squeeze()
    x_array = np.linspace(0, len(input) / 10, len(input))
    for dye in range(number_of_dyes):
        y_max = 20000  # min(1000, 0.1 * max(input[:,dye]))
        y_min = -0.1 * y_max  # always a 10% gap on bottom for legibility
        axes[dye].set_ylim([y_min, y_max])
        plot_markers(Dyes.color_list[dye], axes[dye], y_min, leftoffset)
        line1, = axes[dye].plot(x_array, input[:, dye], "k")

        # plot background of peaks in green
        collection = collections.BrokenBarHCollection.span_where(x_array, ymin=y_min, ymax=y_max,
                                                                 where=labels_peaks[:, dye],
                                                                 facecolor='green', alpha=0.3)
        axes[dye].add_collection(collection)
        # plot background of bins in blue
        collection = collections.BrokenBarHCollection.span_where(x_array, ymin=y_min, ymax=y_max,
                                                                 where=labels_bins[500:5300, dye],
                                                                 facecolor='blue', alpha=0.3)
        axes[dye].add_collection(collection)
        axes[dye].set_xlim([0, 100])
    if not title:
        plt.show()
    else:
        plt.savefig(str(title) + ".png")
    plt.close()
