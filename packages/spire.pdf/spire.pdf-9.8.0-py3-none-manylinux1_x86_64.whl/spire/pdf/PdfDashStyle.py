from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfDashStyle(Enum):
    """
    <summary>
        Possible dash styles of the pen.
    </summary>
    """
    Solid = 0
    Dash = 1
    Dot = 2
    DashDot = 3
    DashDotDot = 4
    Custom = 5
    none = 6

