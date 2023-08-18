from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSubSuperScript(Enum):
    """
    <summary>
        Specifies type of the SubSuperScript.
    </summary>
    """
    none = 0
    SuperScript = 1
    SubScript = 2

