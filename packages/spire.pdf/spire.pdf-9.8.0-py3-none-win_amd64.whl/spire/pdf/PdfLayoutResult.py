from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLayoutResult (SpireObject) :
    """

    """

    @property
    def Page(self)->'PdfPageBase':
        from spire.pdf.PdfPageBase import PdfPageBase
        """

        """
        GetDllLibPdf().PdfLayoutResult_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayoutResult_get_Page.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayoutResult_get_Page(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret
    #@property

    #def Page(self)->SpireObject:
    #    """

    #    """
    #    GetDllLibPdf().PdfLayoutResult_get_Page.argtypes=[c_void_p]
    #    GetDllLibPdf().PdfLayoutResult_get_Page.restype=c_void_p
    #    intPtr = GetDllLibPdf().PdfLayoutResult_get_Page(self.Ptr)
    #    ret = None if intPtr==None else SpireObject(intPtr)
    #    return ret


    @property

    def Bounds(self)->'RectangleF':
        """

        """
        GetDllLibPdf().PdfLayoutResult_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfLayoutResult_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayoutResult_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


