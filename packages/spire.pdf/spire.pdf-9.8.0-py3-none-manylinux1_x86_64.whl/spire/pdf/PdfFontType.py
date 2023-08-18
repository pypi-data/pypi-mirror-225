from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFontType(Enum):
    """
    <summary>
        Specifies the type of the font.
    </summary>
    """
    Standard = 0
    TrueType = 1
    TrueTypeEmbedded = 2

