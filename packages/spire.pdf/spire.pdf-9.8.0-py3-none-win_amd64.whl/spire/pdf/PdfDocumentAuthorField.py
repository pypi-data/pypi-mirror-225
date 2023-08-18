from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfDocumentAuthorField (  PdfSingleValueField) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfDocumentAuthorField_CreatePdfDocumentAuthorField.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDocumentAuthorField_CreatePdfDocumentAuthorField()
        super(PdfDocumentAuthorField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfDocumentAuthorField_CreatePdfDocumentAuthorFieldF.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentAuthorField_CreatePdfDocumentAuthorFieldF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDocumentAuthorField_CreatePdfDocumentAuthorFieldF(ptrFont)
        super(PdfDocumentAuthorField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase,brush:PdfBrush):
        ptrFont:c_void_p = font.Ptr
        ptrBrush:c_void_p = brush.Ptr
        GetDllLibPdf().PdfDocumentAuthorField_CreatePdfDocumentAuthorFieldFB.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfDocumentAuthorField_CreatePdfDocumentAuthorFieldFB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDocumentAuthorField_CreatePdfDocumentAuthorFieldFB(ptrFont,ptrBrush)
        super(PdfDocumentAuthorField, self).__init__(intPtr)

    @dispatch
    def __init__(self, font:PdfFontBase,bounds:RectangleF):
        ptrFont:c_void_p = font.Ptr
        ptrBounds:c_void_p = bounds.Ptr
        GetDllLibPdf().PdfDocumentAuthorField_CreatePdfDocumentAuthorFieldFBs.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfDocumentAuthorField_CreatePdfDocumentAuthorFieldFBs.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDocumentAuthorField_CreatePdfDocumentAuthorFieldFBs(ptrFont,ptrBounds)
        super(PdfDocumentAuthorField, self).__init__(intPtr)
    """
    <summary>
        Represent automatic field which contains document's author name.
    </summary>
    """
