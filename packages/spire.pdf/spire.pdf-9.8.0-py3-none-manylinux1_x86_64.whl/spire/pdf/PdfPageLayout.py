from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPageLayout(Enum):
    """
    <summary>
        A name object specifying the page layout to be used when the
            document is opened.
    </summary>
    """
    SinglePage = 0
    OneColumn = 1
    TwoColumnLeft = 2
    TwoColumnRight = 3
    TwoPageLeft = 4
    TwoPageRight = 5

