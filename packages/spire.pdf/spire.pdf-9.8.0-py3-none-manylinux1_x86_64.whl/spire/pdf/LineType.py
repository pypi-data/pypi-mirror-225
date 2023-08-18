from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class LineType(Enum):
    """
    <summary>
        Break type of the line.
    </summary>
    """
    none = 0
    NewLineBreak = 1
    LayoutBreak = 2
    FirstParagraphLine = 4
    LastParagraphLine = 8

