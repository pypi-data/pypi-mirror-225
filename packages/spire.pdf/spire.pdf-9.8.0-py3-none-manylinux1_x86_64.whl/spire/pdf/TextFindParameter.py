from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class TextFindParameter(Enum):
    """
    <summary>
        Setting find text Parameters
     </summary>
    """
    none = 1
    WholeWord = 16
    IgnoreCase = 256
    Regex = 65536

