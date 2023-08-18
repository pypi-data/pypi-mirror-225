from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAttachmentRelationship(Enum):
    """
    <summary>
         Attachment relationship type.
    </summary>
    """
    Source = 0
    Data = 1
    Alternative = 2
    Supplement = 3
    Unspecified = 4

