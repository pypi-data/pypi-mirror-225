from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFilePathType(Enum):
    """
    <summary>
        Specifies the file path type.
    </summary>
    """
    Relative = 0
    Absolute = 1

