from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfBookletSubsetMode(Enum):
    """
    <summary>
        Pdf print to booklet subset mode
    </summary>
    """
    BothSides = 0
    FrontSide = 1
    ReverseSide = 2

