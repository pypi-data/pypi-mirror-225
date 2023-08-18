from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfMatrixOrder(Enum):
    """
    <summary>
        Represent the applying order to matrix.
    </summary>
    """
    Prepend = 0
    Append = 1

