from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTableDataSourceType(Enum):
    """
    <summary>
        Specifies the datasource type.
    </summary>
    """
    External = 0
    TableDirect = 1

