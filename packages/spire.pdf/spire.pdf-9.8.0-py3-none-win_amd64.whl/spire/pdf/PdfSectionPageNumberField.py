from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSectionPageNumberField (  PdfMultipleNumberValueField) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfSectionPageNumberField_CreatePdfSectionPageNumberField.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSectionPageNumberField_CreatePdfSectionPageNumberField()
        super(PdfSectionPageNumberField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfSectionPageNumberField_CreatePdfSectionPageNumberFieldF.argtypes=[c_void_p]
        GetDllLibPdf().PdfSectionPageNumberField_CreatePdfSectionPageNumberFieldF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSectionPageNumberField_CreatePdfSectionPageNumberFieldF(ptrFont)
        super(PdfSectionPageNumberField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase,brush:PdfBrush):
        ptrFont:c_void_p = font.Ptr
        ptrBrush:c_void_p = brush.Ptr
        GetDllLibPdf().PdfSectionPageNumberField_CreatePdfSectionPageNumberFieldFB.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfSectionPageNumberField_CreatePdfSectionPageNumberFieldFB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSectionPageNumberField_CreatePdfSectionPageNumberFieldFB(ptrFont,ptrBrush)
        super(PdfSectionPageNumberField, self).__init__(intPtr)

    @dispatch
    def __init__(self, font:PdfFontBase,bounds:RectangleF):
        ptrFont:c_void_p = font.Ptr
        ptrBounds:c_void_p = bounds.Ptr
        GetDllLibPdf().PdfSectionPageNumberField_CreatePdfSectionPageNumberFieldFBs.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfSectionPageNumberField_CreatePdfSectionPageNumberFieldFBs.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSectionPageNumberField_CreatePdfSectionPageNumberFieldFBs(ptrFont,ptrBounds)
        super(PdfSectionPageNumberField, self).__init__(intPtr)
    """
    <summary>
        Represents automatic field to display page number within a section.
    </summary>
    """
