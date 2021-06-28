import matplotlib.pyplot as plt


def make_boxplot(dataframe, columns):
    boxplot = dataframe.boxplot(column=columns)
    boxplot.plot()
    plt.ylim([0,1])
    plt.show()