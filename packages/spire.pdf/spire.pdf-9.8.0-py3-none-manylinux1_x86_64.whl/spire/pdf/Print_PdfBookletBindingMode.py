from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Print_PdfBookletBindingMode(Enum):
    """
    <summary>
        Pdf print to booklet binding mode
    </summary>
    """
    Left = 0
    Right = 1
    LeftHigh = 2
    RightHigh = 3

