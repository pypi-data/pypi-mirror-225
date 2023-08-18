from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfMultiPageOrder(Enum):
    """
    <summary>
        Multi pages order in the Paper layout.
    </summary>
    """
    Horizontal = 0
    HorizontalReversed = 1
    Vertical = 2
    VerticalReversed = 3

