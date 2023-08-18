from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfButtonLayoutMode(Enum):
    """
    <summary>
        Represents the button layout mode.
    </summary>
    """
    CaptionOnly = 0
    IconOnly = 1
    CaptionBelowIcon = 2
    CaptionAboveIcon = 3
    CaptionRightOfIcon = 4
    CaptionLeftOfIcon = 5
    CaptionOverlayIcon = 6

