from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class DocType(Enum):
    """
    <summary>
        OOX file type
    </summary>
<author>linyaohu</author>
    """
    Word = 0
    Excel = 1
    Powerpoint = 2
    Unknown = 3

