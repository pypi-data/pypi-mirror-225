from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfHeaderSource(Enum):
    """
    <summary>
        Specifies values specifying where the header should formed from.
    </summary>
    """
    ColumnCaptions = 0
    Rows = 1

