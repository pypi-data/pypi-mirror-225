from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class LoadHtmlType(Enum):
    """
    <summary>
        load from  content type
    </summary>
    """
    URL = 0
    SourceCode = 1

