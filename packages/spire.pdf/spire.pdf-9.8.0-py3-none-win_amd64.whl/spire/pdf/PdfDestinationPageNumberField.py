from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfDestinationPageNumberField (  PdfPageNumberField) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfDestinationPageNumberField_CreatePdfDestinationPageNumberField.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDestinationPageNumberField_CreatePdfDestinationPageNumberField()
        super(PdfDestinationPageNumberField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase):
        ptrFont:c_void_p = font.Ptr
        GetDllLibPdf().PdfDestinationPageNumberField_CreatePdfDestinationPageNumberFieldF.argtypes=[c_void_p]
        GetDllLibPdf().PdfDestinationPageNumberField_CreatePdfDestinationPageNumberFieldF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDestinationPageNumberField_CreatePdfDestinationPageNumberFieldF(ptrFont)
        super(PdfDestinationPageNumberField, self).__init__(intPtr)
    @dispatch
    def __init__(self, font:PdfFontBase,brush:PdfBrush):
        ptrFont:c_void_p = font.Ptr
        ptrBrush:c_void_p = brush.Ptr
        GetDllLibPdf().PdfDestinationPageNumberField_CreatePdfDestinationPageNumberFieldFB.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfDestinationPageNumberField_CreatePdfDestinationPageNumberFieldFB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDestinationPageNumberField_CreatePdfDestinationPageNumberFieldFB(ptrFont,ptrBrush)
        super(PdfDestinationPageNumberField, self).__init__(intPtr)

    @dispatch
    def __init__(self, font:PdfFontBase,bounds:RectangleF):
        ptrFont:c_void_p = font.Ptr
        ptrBounds:c_void_p = bounds.Ptr
        GetDllLibPdf().PdfDestinationPageNumberField_CreatePdfDestinationPageNumberFieldFBs.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfDestinationPageNumberField_CreatePdfDestinationPageNumberFieldFBs.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDestinationPageNumberField_CreatePdfDestinationPageNumberFieldFBs(ptrFont,ptrBounds)
        super(PdfDestinationPageNumberField, self).__init__(intPtr)
    """
    <summary>
        Represents class which displays destination page's number.
    </summary>
    """
    @property

    def PageWidget(self)->'PdfPageWidget':
        """
    <summary>
        Get and sets the PdfLoadedPage
    </summary>
        """
        GetDllLibPdf().PdfDestinationPageNumberField_get_PageWidget.argtypes=[c_void_p]
        GetDllLibPdf().PdfDestinationPageNumberField_get_PageWidget.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDestinationPageNumberField_get_PageWidget(self.Ptr)
        ret = None if intPtr==None else PdfPageWidget(intPtr)
        return ret


    @PageWidget.setter
    def PageWidget(self, value:'PdfPageWidget'):
        GetDllLibPdf().PdfDestinationPageNumberField_set_PageWidget.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDestinationPageNumberField_set_PageWidget(self.Ptr, value.Ptr)

    @property

    def Page(self)->'PdfNewPage':
        """
    <summary>
        Gets or sets the page.
    </summary>
<value>The page.</value>
        """
        GetDllLibPdf().PdfDestinationPageNumberField_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().PdfDestinationPageNumberField_get_Page.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDestinationPageNumberField_get_Page(self.Ptr)
        ret = None if intPtr==None else PdfNewPage(intPtr)
        return ret


    @Page.setter
    def Page(self, value:'PdfNewPage'):
        GetDllLibPdf().PdfDestinationPageNumberField_set_Page.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDestinationPageNumberField_set_Page(self.Ptr, value.Ptr)

