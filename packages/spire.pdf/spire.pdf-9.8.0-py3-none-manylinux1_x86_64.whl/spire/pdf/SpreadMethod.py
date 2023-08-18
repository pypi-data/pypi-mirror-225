from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class SpreadMethod(Enum):
    """
<remarks />
    """
    Pad = 0
    Reflect = 1
    Repeat = 2
    none = 3

