from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XmpArrayType(Enum):
    """
    <summary>
        Types of the xmp arrays.
    </summary>
    """
    Unknown = 0
    Bag = 1
    Seq = 2
    Alt = 3

