from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfDateTimeField (  PdfStaticField) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfDateTimeField_CreatePdfDateTimeField.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDateTimeField_CreatePdfDateTimeField()
        super(PdfDateTimeField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfDateTimeField_CreatePdfDateTimeFieldF.argtypes=[c_void_p]
        GetDllLibPdf().PdfDateTimeField_CreatePdfDateTimeFieldF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDateTimeField_CreatePdfDateTimeFieldF(ptrFont)
        super(PdfDateTimeField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase,brush:PdfBrush):
        ptrFont:c_void_p = font.Ptr
        ptrBrush:c_void_p = brush.Ptr
        GetDllLibPdf().PdfDateTimeField_CreatePdfDateTimeFieldFB.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfDateTimeField_CreatePdfDateTimeFieldFB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDateTimeField_CreatePdfDateTimeFieldFB(ptrFont,ptrBrush)
        super(PdfDateTimeField, self).__init__(intPtr)

    @dispatch
    def __init__(self, font:PdfFontBase,bounds:RectangleF):
        ptrFont:c_void_p = font.Ptr
        ptrBounds:c_void_p = bounds.Ptr
        GetDllLibPdf().PdfDateTimeField_CreatePdfDateTimeFieldFBs.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfDateTimeField_CreatePdfDateTimeFieldFBs.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDateTimeField_CreatePdfDateTimeFieldFBs(ptrFont,ptrBounds)
        super(PdfDateTimeField, self).__init__(intPtr)
    """
    <summary>
        Represents date automated field.
    </summary>
    """
    @property

    def DateFormatString(self)->str:
        """
    <summary>
        Gets or sets the format string.
    </summary>
<value>The format string.</value>
        """
        GetDllLibPdf().PdfDateTimeField_get_DateFormatString.argtypes=[c_void_p]
        GetDllLibPdf().PdfDateTimeField_get_DateFormatString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfDateTimeField_get_DateFormatString(self.Ptr))
        return ret


    @DateFormatString.setter
    def DateFormatString(self, value:str):
        GetDllLibPdf().PdfDateTimeField_set_DateFormatString.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfDateTimeField_set_DateFormatString(self.Ptr, value)

