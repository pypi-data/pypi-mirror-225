from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ItemsChoiceType(Enum):
    """
<remarks />
    """
    FigureStructure = 0
    ListStructure = 1
    ParagraphStructure = 2
    TableStructure = 3

