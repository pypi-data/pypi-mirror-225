from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class TabOrder(Enum):
    """
    <summary>
        A name specifying the tab order to be used for annotations on the page.
    </summary>
    """
    Row = 0
    Column = 1
    Structure = 2
    Unspecified = 3

