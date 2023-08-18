from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCrossReferenceType(Enum):
    """
    <summary>
        Specifies the type of the PDF cross-reference.
    </summary>
<remarks>Default value is CrossReferenceStream</remarks>
    """
    CrossReferenceTable = 0
    CrossReferenceStream = 1

