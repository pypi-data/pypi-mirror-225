from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XmpStructureType(Enum):
    """
    <summary>
        Enumerates types of the xmp structure.
    </summary>
    """
    Dimensions = 0
    Font = 1
    Colorant = 2
    Thumbnail = 3
    Job = 4

