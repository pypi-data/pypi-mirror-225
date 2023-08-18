from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfVisibility(Enum):
    """
    <summary>
        Represent the visibility of optional content group(or optional content membership).
    </summary>
    """
    On = 0
    Off = 1

