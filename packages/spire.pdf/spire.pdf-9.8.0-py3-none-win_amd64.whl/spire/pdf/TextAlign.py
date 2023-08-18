from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class TextAlign(Enum):
    """
    <summary>
        Specifies how text in a  is
            horizontally aligned.
    </summary>
    """
    Left = 1
    Right = 2
    Center = 3
    Justify = 4

