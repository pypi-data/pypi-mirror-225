from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextStyle(Enum):
    """
    <summary>
        Allows to choose outline text style.
    </summary>
    """
    Regular = 0
    Italic = 1
    Bold = 2

