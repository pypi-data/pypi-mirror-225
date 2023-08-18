from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFillMode(Enum):
    """
    <summary>
        Specifies how the shapes are filled. 
    </summary>
    """
    Winding = 0
    Alternate = 1

