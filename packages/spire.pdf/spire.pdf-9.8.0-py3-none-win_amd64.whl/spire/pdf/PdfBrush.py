from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfBrush (SpireObject) :
    """
    <summary>
        Represents the abstract brush, which containing a basic functionality of a brush.
    </summary>
    """

    def Clone(self)->'PdfBrush':
        """
    <summary>
        Creates a new copy of a brush.
    </summary>
    <returns>A new instance of the Brush class.</returns>
        """
        GetDllLibPdf().PdfBrush_Clone.argtypes=[c_void_p]
        GetDllLibPdf().PdfBrush_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBrush_Clone(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


