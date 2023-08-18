from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSinglePageScalingMode(Enum):
    """
    <summary>
        Pdf Print Page Scale type
    </summary>
    """
    FitSize = 0
    ActualSize = 1
    ShrinkOversized = 2
    CustomScale = 3

