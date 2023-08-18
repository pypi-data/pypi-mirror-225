from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextLayout (SpireObject) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfTextLayout_CreatePdfTextLayout.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTextLayout_CreatePdfTextLayout()
        super(PdfTextLayout, self).__init__(intPtr)

    @dispatch
    def __init__(self, baseFormat:'PdfTextLayout'):
        ptrbaseFormat:c_void_p = baseFormat.Ptr
        GetDllLibPdf().PdfTextLayout_CreatePdfTextLayoutB.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextLayout_CreatePdfTextLayoutB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTextLayout_CreatePdfTextLayoutB(ptrbaseFormat)
        super(PdfTextLayout, self).__init__(intPtr)
    """

    """
    @property

    def Layout(self)->'PdfLayoutType':
        """

        """
        GetDllLibPdf().PdfTextLayout_get_Layout.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextLayout_get_Layout.restype=c_int
        ret = GetDllLibPdf().PdfTextLayout_get_Layout(self.Ptr)
        objwraped = PdfLayoutType(ret)
        return objwraped

    @Layout.setter
    def Layout(self, value:'PdfLayoutType'):
        GetDllLibPdf().PdfTextLayout_set_Layout.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfTextLayout_set_Layout(self.Ptr, value.value)

    @property

    def Break(self)->'PdfLayoutBreakType':
        """

        """
        GetDllLibPdf().PdfTextLayout_get_Break.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextLayout_get_Break.restype=c_int
        ret = GetDllLibPdf().PdfTextLayout_get_Break(self.Ptr)
        objwraped = PdfLayoutBreakType(ret)
        return objwraped

    @Break.setter
    def Break(self, value:'PdfLayoutBreakType'):
        GetDllLibPdf().PdfTextLayout_set_Break.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfTextLayout_set_Break(self.Ptr, value.value)

    @property

    def PaginateBounds(self)->'RectangleF':
        """

        """
        GetDllLibPdf().PdfTextLayout_get_PaginateBounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextLayout_get_PaginateBounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTextLayout_get_PaginateBounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @PaginateBounds.setter
    def PaginateBounds(self, value:'RectangleF'):
        GetDllLibPdf().PdfTextLayout_set_PaginateBounds.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfTextLayout_set_PaginateBounds(self.Ptr, value.Ptr)

