from dataclasses import dataclass
from typing import List, Dict
import numpy as np
import xml.etree.ElementTree as eT


@dataclass
class Dye:
    """ Class for fluorescent dyes of genetic analyzer."""
    name: str           # example: 'FL-6C'
    plot_color: str     # example: 'b'
    plot_index: int     # index of which of 6 subplots when all dyes\
                        # are plotted in the same image\


@dataclass
class Dyes:
    BLUE = Dye('FL-6C', 'b', 1)
    GREEN = Dye('JOE-6C', 'g', 2)
    YELLOW = Dye('TMR-6C', 'k', 3)      # usually plotted in black for visibility
    RED = Dye('CXR-6C', 'r', 4)
    PURPLE = Dye('TOM-6C', 'm', 5)
    SIZESTD = Dye('WEN-6C', 'orange', 6)
    color_list = [BLUE, GREEN, YELLOW, RED, PURPLE, SIZESTD]


@dataclass
class Allele:
    """Class for each allele that can be identified."""
    name: str       # example: 'X' or '17'
    mid: float      # horizontal position, example: '87.32'
    left: float     # left side of bin from mid (0.4 or 0.5)
    right: float    # right side of bin from mid (0.4 or 0.5)
    dye: Dye        # or add locus?


@dataclass
class Locus:
    """Class for locus, stores Alleles per locus in dict."""
    alleles: Dict[str, Allele]      # example of entry: '18': Allele
    name: str                       # example: 'AMEL'
    dye: Dye                        # dye that locus is on
    lower: float                    # lower boundary of marker
    upper: float                    # upper boundary of marker


@dataclass
class Loci:
    def create_dict(self):
        """Read xml file for bins of each allele, \
        returns dictionary of information"""
        tree_file = eT.parse("data/PPF6C_SPOOR.xml")
        root = tree_file.getroot()
        locus_dict = {}
        # root[5] is the node with loci, rest is panel info
        for locus in root[5]:
            locus_name = locus.find('MarkerTitle').text
            # to translate the numbers in xml file to dyes
            temp_dict = {1: Dyes.BLUE, 2: Dyes.GREEN, 3: Dyes.YELLOW, 4: Dyes.RED, 5: Dyes.SIZESTD, 6: Dyes.PURPLE}
            dye = int(locus.find('DyeIndex').text)
            lower = float(locus.find('LowerBoundary').text)
            upper = float(locus.find('UpperBoundary').text)
            # store info so far in Locus dataclass
            new_locus = Locus({}, locus_name, temp_dict[dye], lower, upper)
            # add all alleles to locus
            for allele in locus.findall('Allele'):
                allele_name = allele.get('Label')
                mid = float(allele.get('Size'))
                left = float(allele.get('Left_Binning'))
                right = float(allele.get('Right_Binning'))
                # store in Allele dataclass
                new_allele = Allele(allele_name, mid, left, right, temp_dict[dye])
                # add to alleles dict of locus
                new_locus.alleles[allele_name] = new_allele
            # add created locus to locus dict
            locus_dict[locus_name] = new_locus
        return locus_dict


# global variable
locus_dict = Loci().create_dict()


@dataclass
class Peak:
    """Class for an identified or expected allele peak.
    Has everything needed for plotting."""
    allele: Allele
    height: float   # height of peak


@dataclass
class Sample:
    """
    Class for samples, data is (nx6) matrix of all 6 colours
    """
    name: str       # example: '1A2'
    replica: int
    data: List


@dataclass
class Person:
    """ Class to store alleles a Person has. """
    name: str            # name is A - Z, letter used to identify person
    alleles: List[str]   # list of 'locus_allele' names


@dataclass
class PersonMixture:
    name: str                       # for example: "1A2"
    # donor_set: str                  # "1"
    # mixture_type: str               # "A"
    # number_of_donors: int           # 2
    persons: List[Person]           # list of Persons present in mix
    fractions: Dict[str, float]     # fractional contribution of each person in mixture

    def create_peaks(self):
        """Returns list of peaks expected in mixture and their relative heights"""
        peak_list = []
        peak_dict = {}
        # add X and Y by hand (all samples are male)
        X_and_Y = locus_dict['AMEL']
        X = X_and_Y.alleles['X']
        Y = X_and_Y.alleles['Y']
        peak_list.append(Peak(X, 0.5))
        peak_list.append(Peak(Y, 0.5))
        # iterate through persons in mix
        for person in self.persons:
            # iterate over their alleles
            for locus_allele in person.alleles:
                if locus_allele in peak_dict:
                    peak_dict[locus_allele] += self.fractions[person.name]
                else:
                    peak_dict[locus_allele] = self.fractions[person.name]
        # now we have a dictionary of the height of the alleles
        # all that's left is to store corresponding peaks in list
        for locus_allele in peak_dict:
            locus_name, allele_name = locus_allele.split("_")
            locus = locus_dict[locus_name]
            allele = locus.alleles[allele_name]
            height = peak_dict[locus_allele]        # store rel. height
            new_peak = Peak(allele, height)
            peak_list.append(new_peak)               # append peak to list
        return peak_list


@dataclass
class AnalystMixture:
    """ Class to store peaks identified in mixture. """
    name: str               # name of mixture, '1A2' for example
    replica: int            # where 1 is donor set, 2 is #donors, A is mixture type and 3 is replica
    peaks: List[Peak]       # list of peaks


# TBD ############################################################################
@dataclass
class Center:
    """class to store center of input to be labeled"""
    index: float    # nucleotide location
    dye: Dye        # dye in which center is present


@dataclass
class TrainInput:
    input_sample: Sample          # sample used to create input
    data: np.ndarray              # list of input nodes/data to be fed to nn
    labels: np.ndarray            # list of labels corresponding to data


@dataclass
class TrainOutput:
    input_sample: Sample
    labels: List

@dataclass
class TestInput:
    """Class for input without labels to test on."""
    # turns out the convnet also takes the labels of the test set as input
    name: str


@dataclass
class Result:
    """ TBD """
    name: str


# Global variables
PICOGRAMS = np.array([[300, 150, 150, 150, 150],
                      [300, 30,  30,  30,  30],
                      [150, 150, 60,  60,  60],
                      [150, 30,  60,  30,  30],
                      [600, 30,  60,  30,  30]])

TOTAL_PICOGRAMS = np.array([[450, 600, 750, 900],
                            [330, 360, 390, 420],
                            [300, 360, 420, 480],
                            [180, 240, 270, 300],
                            [630, 690, 720, 750]])

