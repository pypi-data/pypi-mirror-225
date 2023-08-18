from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DActivationMode(Enum):
    """
    <summary>
        Specifies the available modes for activating a 3D annotation. 
    </summary>
    """
    PageOpen = 0
    PageVisible = 1
    ExplicitActivation = 2

