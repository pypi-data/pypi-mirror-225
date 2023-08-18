from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLineIntent(Enum):
    """
    <summary>
        Specifies the Line Intent Style is to be used in the Line annotation.
    </summary>
    """
    LineArrow = 0
    LineDimension = 1

