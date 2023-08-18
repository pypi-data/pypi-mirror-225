from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class CompressionMethod(Enum):
    """

    """
    Stored = 0
    Shrunk = 1
    ReducedFactor1 = 2
    ReducedFactor2 = 3
    ReducedFactor3 = 4
    ReducedFactor4 = 5
    Imploded = 6
    Tokenizing = 7
    Deflated = 8
    Defalte64 = 9
    PRWARE = 10
    BZIP2 = 12
    LZMA = 14
    IBMTerse = 18
    LZ77 = 19
    PPMd = 98

