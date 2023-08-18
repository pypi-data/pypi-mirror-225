from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class StyleSimulations(Enum):
    """
<remarks />
    """
    none = 0
    ItalicSimulation = 1
    BoldSimulation = 2
    BoldItalicSimulation = 3

