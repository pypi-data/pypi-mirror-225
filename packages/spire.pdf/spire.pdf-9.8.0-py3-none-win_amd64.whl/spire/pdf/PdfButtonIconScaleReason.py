from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfButtonIconScaleReason(Enum):
    """
    <summary>
        Represtents the circumstances under which the icon shall be scaled inside the annotation rectangle.
    </summary>
    """
    Always = 0
    IconIsBigger = 1
    IconIsSmaller = 2
    Never = 3

