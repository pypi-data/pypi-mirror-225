from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextLayoutResult (  PdfLayoutResult) :
    """

    """
    @property

    def Remainder(self)->str:
        """

        """
        GetDllLibPdf().PdfTextLayoutResult_get_Remainder.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextLayoutResult_get_Remainder.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextLayoutResult_get_Remainder(self.Ptr))
        return ret


    @property

    def LastLineBounds(self)->'RectangleF':
        """

        """
        GetDllLibPdf().PdfTextLayoutResult_get_LastLineBounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextLayoutResult_get_LastLineBounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTextLayoutResult_get_LastLineBounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


