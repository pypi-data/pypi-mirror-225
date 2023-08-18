from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class HttpMethod(Enum):
    """
    <summary>
        Specifies Http request method.
    </summary>
    """
    Get = 0
    Post = 1

