from dataclasses import dataclass
from typing import List, Dict
import numpy as np


# Global variables
#   A: 	300:150	300:150:150	300:150:150:150	300:150:150:150:150
#   B: 	300:30	300:30:30	300:30:30:30	300:30:30:30:30
#   C: 	150:150	150:150:60	150:150:60:60	150:150:60:60:60
#   D:	150:30	150:30:60	150:30:60:30	150:30:60:30:30
#   E:	600:30	600:30:60	600:30:60:30	600:30:60:30:30

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


@dataclass
class Dye:
    """ Class for fluorescent dyes of genetic analyzer."""
    name: str           # example: 'FL-6C'
    plot_color: str     # example: 'b'
    plot_index: int     # index of which of 6 subplots when all dyes\
                        # are plotted in the same image


@dataclass
class Allele:
    """Class for each allele that can be identified."""
    name: str       # example: 'X' or '17'
    mid: float      # horizontal position, example: '87.32'
    left: float     # left side of bin from mid (0.4 or 0.5)
    right: float    # right side of bin from mid (0.4 or 0.5)
    height: float   # height of peak at allele
    # note: left_binning is not always equal to right_binning


@dataclass
class Locus:
    """Class for locus, stores Alleles per locus in dict."""
    alleles: Dict[str, Allele]      # example of entry: '18': Allele()
    name: str                       # example: 'AMEL'
    dye: Dye                        #
    lower: float                    # lower boundary of marker
    upper: float                    # upper boundary of marker


@dataclass
class Sample:
    """
    Class for samples, data is (nx6) matrix of all 6 colours
    Should I split this into a list per color attribute?
    Should I add the color_list here instead of in pf? Only used icw Samples for ordering
    """
    name: str       # example: '1A2'
    data: List      #


@dataclass
class Person:
    """ Class to store alleles a Person has. """
    name: str            # name is A - Z, letter used to identify person
    alleles: List[str]   # list of 'locus_allele' names


@dataclass
class Mixture:
    """ Class to store peaks identified/expected in mixture. """
    name: str               # name of mixture, '1A2' for example
    alleles: List[str]      # list of locus_allele names (e.g. 'AMEL_X')
    heights: List[float]    # heights can either be relative (0-1) or absolute (in rfu)


# misschien uiteindelijk:
# output class/geanalyseerd profiel, welke pieken zijn aangewezen door CNN
@dataclass
class Result:
    """ TBD """
    name: str
    peaks: Dict[Locus, float]
    thresholds: List[float]
