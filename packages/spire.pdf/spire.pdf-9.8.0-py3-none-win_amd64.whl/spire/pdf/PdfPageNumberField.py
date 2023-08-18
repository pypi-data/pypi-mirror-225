from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPageNumberField (  PdfMultipleNumberValueField) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfPageNumberField_CreatePdfPageNumberField.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPageNumberField_CreatePdfPageNumberField()
        super(PdfPageNumberField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfPageNumberField_CreatePdfPageNumberFieldF.argtypes=[c_void_p]
        GetDllLibPdf().PdfPageNumberField_CreatePdfPageNumberFieldF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPageNumberField_CreatePdfPageNumberFieldF(ptrFont)
        super(PdfPageNumberField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase,brush:PdfBrush):
        ptrFont:c_void_p = font.Ptr
        ptrBrush:c_void_p = brush.Ptr
        GetDllLibPdf().PdfPageNumberField_CreatePdfPageNumberFieldFB.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfPageNumberField_CreatePdfPageNumberFieldFB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPageNumberField_CreatePdfPageNumberFieldFB(ptrFont,ptrBrush)
        super(PdfPageNumberField, self).__init__(intPtr)

    @dispatch
    def __init__(self, font:PdfFontBase,bounds:RectangleF):
        ptrFont:c_void_p = font.Ptr
        ptrBounds:c_void_p = bounds.Ptr
        GetDllLibPdf().PdfPageNumberField_CreatePdfPageNumberFieldFBs.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfPageNumberField_CreatePdfPageNumberFieldFBs.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPageNumberField_CreatePdfPageNumberFieldFBs(ptrFont,ptrBounds)
        super(PdfPageNumberField, self).__init__(intPtr)
    """
    <summary>
        Represents page number field.
    </summary>
    """
