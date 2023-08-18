from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCreationDateField (  PdfSingleValueField) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfCreationDateField_CreatePdfCreationDateField.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCreationDateField_CreatePdfCreationDateField()
        super(PdfCreationDateField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfCreationDateField_CreatePdfCreationDateFieldF.argtypes=[c_void_p]
        GetDllLibPdf().PdfCreationDateField_CreatePdfCreationDateFieldF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCreationDateField_CreatePdfCreationDateFieldF(ptrFont)
        super(PdfCreationDateField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase,brush:PdfBrush):
        ptrFont:c_void_p = font.Ptr
        ptrBrush:c_void_p = brush.Ptr
        GetDllLibPdf().PdfCreationDateField_CreatePdfCreationDateFieldFB.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfCreationDateField_CreatePdfCreationDateFieldFB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCreationDateField_CreatePdfCreationDateFieldFB(ptrFont,ptrBrush)
        super(PdfCreationDateField, self).__init__(intPtr)

    @dispatch
    def __init__(self, font:PdfFontBase,bounds:RectangleF):
        ptrFont:c_void_p = font.Ptr
        ptrBounds:c_void_p = bounds.Ptr
        GetDllLibPdf().PdfCreationDateField_CreatePdfCreationDateFieldFBs.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfCreationDateField_CreatePdfCreationDateFieldFBs.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCreationDateField_CreatePdfCreationDateFieldFBs(ptrFont,ptrBounds)
        super(PdfCreationDateField, self).__init__(intPtr)
    """
    <summary>
        Represents class to display creation date of the document.
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
        GetDllLibPdf().PdfCreationDateField_get_DateFormatString.argtypes=[c_void_p]
        GetDllLibPdf().PdfCreationDateField_get_DateFormatString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfCreationDateField_get_DateFormatString(self.Ptr))
        return ret


    @DateFormatString.setter
    def DateFormatString(self, value:str):
        GetDllLibPdf().PdfCreationDateField_set_DateFormatString.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfCreationDateField_set_DateFormatString(self.Ptr, value)

