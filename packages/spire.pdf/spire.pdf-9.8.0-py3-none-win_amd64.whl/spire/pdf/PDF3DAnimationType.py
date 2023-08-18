from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PDF3DAnimationType(Enum):
    """
    <summary>
        Specifies the available animation style for rendering the 3D artwork. 
    </summary>
    """
    none = 0
    Linear = 1
    Oscillating = 2

