from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLineBorderStyle(Enum):
    """
    <summary>
        Specifies the Line Border Style is to be used in the Line annotation.
    </summary>
    """
    Solid = 0
    Dashed = 1
    Beveled = 2
    Inset = 3
    Underline = 4

