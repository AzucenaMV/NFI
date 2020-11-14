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
    marker: str
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
    data: List


@dataclass
class Person:
    name: str
    alleles: List[Allele]


@dataclass
class Mixture:
    name: str
    alleles: List[Allele]
    heights: List[float]


# misschien uiteindelijk:
# output class/geanalyseerd profiel, welke pieken zijn aangewezen door CNN
@dataclass
class Result:
    name: str
    # something to store peaks and heights
    peaks: Dict[Locus, float]
    thresholds: List[float]
