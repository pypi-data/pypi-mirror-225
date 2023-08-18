from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfDynamicField (  PdfAutomaticField) :
    """
    <summary>
        Represents automatic field which value is dynamically evaluated.
    </summary>
    """
