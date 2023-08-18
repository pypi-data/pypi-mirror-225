from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfVerticalAlignment(Enum):
    """
    <summary>
        Specifies the type of Vertical alignment.
    </summary>
    """
    Top = 0
    Middle = 1
    Bottom = 2

