from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPrinterResolutionKind(Enum):
    """
    <summary>
         Specifies a printer resolution kind.
    </summary>
    """
    High = -4
    Medium = -3
    Low = -2
    Draft = -1
    Custom = 0

