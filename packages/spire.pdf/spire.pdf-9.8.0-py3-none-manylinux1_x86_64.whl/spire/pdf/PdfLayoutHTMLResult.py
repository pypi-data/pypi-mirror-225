from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLayoutHTMLResult (  PdfLayoutResult) :
    """

    """
    @property

    def HTMLViewBounds(self)->'RectangleF':
        """
    <summary>
        The actual bounds of the html view. It may larger than Bounds
    </summary>
        """
        GetDllLibPdf().PdfLayoutHTMLResult_get_HTMLViewBounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayoutHTMLResult_get_HTMLViewBounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayoutHTMLResult_get_HTMLViewBounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


