from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class LayerPrintState(Enum):
    """
    <summary>
        Specifies the print state of the Layer
    </summary>
    """
    Allways = 0
    Nerver = 1
    PrintWhenVisible = 2

