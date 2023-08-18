from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSectionPageCountField (  PdfMultipleNumberValueField) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfSectionPageCountField_CreatePdfSectionPageCountField.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSectionPageCountField_CreatePdfSectionPageCountField()
        super(PdfSectionPageCountField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfSectionPageCountField_CreatePdfSectionPageCountFieldF.argtypes=[c_void_p]
        GetDllLibPdf().PdfSectionPageCountField_CreatePdfSectionPageCountFieldF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSectionPageCountField_CreatePdfSectionPageCountFieldF(ptrFont)
        super(PdfSectionPageCountField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase,brush:PdfBrush):
        ptrFont:c_void_p = font.Ptr
        ptrBrush:c_void_p = brush.Ptr
        GetDllLibPdf().PdfSectionPageCountField_CreatePdfSectionPageCountFieldFB.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfSectionPageCountField_CreatePdfSectionPageCountFieldFB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSectionPageCountField_CreatePdfSectionPageCountFieldFB(ptrFont,ptrBrush)
        super(PdfSectionPageCountField, self).__init__(intPtr)

    @dispatch
    def __init__(self, font:PdfFontBase,bounds:RectangleF):
        ptrFont:c_void_p = font.Ptr
        ptrBounds:c_void_p = bounds.Ptr
        GetDllLibPdf().PdfSectionPageCountField_CreatePdfSectionPageCountFieldFBs.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfSectionPageCountField_CreatePdfSectionPageCountFieldFBs.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSectionPageCountField_CreatePdfSectionPageCountFieldFBs(ptrFont,ptrBounds)
        super(PdfSectionPageCountField, self).__init__(intPtr)
    """
    <summary>
        Represents automatic field to display number of pages in section.
    </summary>
    """
