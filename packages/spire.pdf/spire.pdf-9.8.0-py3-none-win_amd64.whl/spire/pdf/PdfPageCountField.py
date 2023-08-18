from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPageCountField (  PdfSingleValueField) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfPageCountField_CreatePdfPageCountField.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPageCountField_CreatePdfPageCountField()
        super(PdfPageCountField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfPageCountField_CreatePdfPageCountFieldF.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageCountField_CreatePdfPageCountFieldF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPageCountField_CreatePdfPageCountFieldF(ptrFont)
        super(PdfPageCountField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase,brush:PdfBrush):
        ptrFont:c_void_p = font.Ptr
        ptrBrush:c_void_p = brush.Ptr
        GetDllLibPdf().PdfPageCountField_CreatePdfPageCountFieldFB.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfPageCountField_CreatePdfPageCountFieldFB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPageCountField_CreatePdfPageCountFieldFB(ptrFont,ptrBrush)
        super(PdfPageCountField, self).__init__(intPtr)

    @dispatch
    def __init__(self, font:PdfFontBase,bounds:RectangleF):
        ptrFont:c_void_p = font.Ptr
        ptrBounds:c_void_p = bounds.Ptr
        GetDllLibPdf().PdfPageCountField_CreatePdfPageCountFieldFBs.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfPageCountField_CreatePdfPageCountFieldFBs.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPageCountField_CreatePdfPageCountFieldFBs(ptrFont,ptrBounds)
        super(PdfPageCountField, self).__init__(intPtr)
    """
    <summary>
        Represents total page count automatic field.
    </summary>
    """
    @property

    def NumberStyle(self)->'PdfNumberStyle':
        """
    <summary>
        Gets or sets the number style.
    </summary>
<value>The number style.</value>
        """
        GetDllLibPdf().PdfPageCountField_get_NumberStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageCountField_get_NumberStyle.restype=c_int
        ret = GetDllLibPdf().PdfPageCountField_get_NumberStyle(self.Ptr)
        objwraped = PdfNumberStyle(ret)
        return objwraped

    @NumberStyle.setter
    def NumberStyle(self, value:'PdfNumberStyle'):
        GetDllLibPdf().PdfPageCountField_set_NumberStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPageCountField_set_NumberStyle(self.Ptr, value.value)

