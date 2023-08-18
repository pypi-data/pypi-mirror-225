from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFontFamily(Enum):
    """
    <summary>
        Indicates type of standard PDF fonts.
    </summary>
    """
    Helvetica = 0
    Courier = 1
    TimesRoman = 2
    Symbol = 3
    ZapfDingbats = 4

