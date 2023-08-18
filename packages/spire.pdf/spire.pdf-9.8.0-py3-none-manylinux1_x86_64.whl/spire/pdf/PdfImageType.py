from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfImageType(Enum):
    """
    <summary>
        Specifies the type of the PdfImage.
    </summary>
    """
    Bitmap = 0
    #Metafile = 1

