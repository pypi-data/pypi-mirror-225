from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XmpSchemaType(Enum):
    """
    <summary>
        Enumerates types of the xmp schema.
    </summary>
    """
    DublinCoreSchema = 0
    BasicSchema = 1
    RightsManagementSchema = 2
    BasicJobTicketSchema = 3
    PagedTextSchema = 4
    PDFSchema = 5
    Custom = 6

