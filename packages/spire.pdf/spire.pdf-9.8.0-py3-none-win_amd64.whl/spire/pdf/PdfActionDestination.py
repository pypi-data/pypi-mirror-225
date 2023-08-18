from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfActionDestination(Enum):
    """
    <summary>
        Specifies the available named actions supported by the viewer. 
    </summary>
    """
    FirstPage = 0
    LastPage = 1
    NextPage = 2
    PrevPage = 3

