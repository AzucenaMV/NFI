from dataclasses import dataclass
from typing import List, Dict
import numpy as np


# Global variables
#   A: 	300:150	300:150:150	300:150:150:150	300:150:150:150:150
#   B: 	300:30	300:30:30	300:30:30:30	300:30:30:30:30
#   C: 	150:150	150:150:60	150:150:60:60	150:150:60:60:60
#   D:	150:30	150:30:60	150:30:60:30	150:30:60:30:30
#   E:	600:30	600:30:60	600:30:60:30	600:30:60:30:30

picograms = np.array([[300, 150, 150, 150, 150],
                      [300, 30,  30,  30,  30],
                      [150, 150, 60,  60,  60],
                      [150, 30,  60,  30,  30],
                      [600, 30,  60,  30,  30]])

total_picograms = np.array([[450, 600, 750, 900],
                            [330, 360, 390, 420],
                            [300, 360, 420, 480],
                            [180, 240, 270, 300],
                            [630, 690, 720, 750]])


@dataclass
class Dye:
    name: str
    plot_color: str
    plot_index: int


@dataclass
class Allele:
    name: str
    mid: float
    left: float
    right: float
    height: float
    # note: leftbinning is not always equal to rightbinning
    # also, not always 0.5, sometimes 0.4


@dataclass
class Locus:
    """ Alleles per locus are stored in dict for easy access """
    alleles: Dict[str, Allele]
    name: str
    dye: Dye
    lower: float
    upper: float


@dataclass
class Sample:
    """
    Class for samples, data is (nx6) matrix of all 6 colours
    Should I split this into a list per color attribute?
    Should I add the color_list here instead of in pf? Only used icw Samples for ordering
    """
    name: str
    # actually a numpy array of nx6, but this seems to work?
    data: List


@dataclass
class Person:
    """ Class to store alleles a Person has. """
    name: str               # name is A - Z, letter used to identify person
    alleles: List[Allele]   # list of alleles


@dataclass
class Mixture:
    """ Class to store peaks identified/expected in mixture. """
    name: str               # name of mixture, '1A2' for example
    alleles: List[str]      # alleles is a list of locus_allele names (e.g. 'AMEL_X')
    heights: List[float]    # heights can either be relative (0-1) or absolute (in rfu)


# misschien uiteindelijk:
# output class/geanalyseerd profiel, welke pieken zijn aangewezen door CNN
@dataclass
class Result:
    """ TBD """
    name: str
    peaks: Dict[Locus, float]
    thresholds: List[float]
