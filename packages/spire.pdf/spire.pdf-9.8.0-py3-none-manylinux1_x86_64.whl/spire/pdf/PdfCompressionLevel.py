from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCompressionLevel(Enum):
    """
    <summary>
        Defines data compression level.
    </summary>
    """
    none = 0
    BestSpeed = 1
    BelowNormal = 3
    Normal = 5
    AboveNormal = 7
    Best = 9

