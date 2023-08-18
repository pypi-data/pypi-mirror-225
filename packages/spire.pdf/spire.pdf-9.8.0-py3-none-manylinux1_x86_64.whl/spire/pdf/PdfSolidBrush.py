from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSolidBrush (  PdfBrush) :
    @dispatch
    def __init__(self, color:PdfRGBColor):

        ptrColor:c_void_p = color.Ptr
        GetDllLibPdf().PdfSolidBrush_CreatePdfSolidBrushRC.argtypes=[c_void_p]
        GetDllLibPdf().PdfSolidBrush_CreatePdfSolidBrushRC.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSolidBrush_CreatePdfSolidBrushRC(ptrColor)
        super(PdfSolidBrush, self).__init__(intPtr)
    @dispatch
    def __init__(self, color:PdfComplexColor):
        ptrColor:c_void_p = color.Ptr
        GetDllLibPdf().PdfSolidBrush_CreatePdfSolidBrushCC.argtypes=[c_void_p]
        GetDllLibPdf().PdfSolidBrush_CreatePdfSolidBrushCC.restype = c_void_p
        intPtr = GetDllLibPdf().PdfSolidBrush_CreatePdfSolidBrushCC(ptrColor)
        super(PdfSolidBrush, self).__init__(intPtr)
    """
    <summary>
        Represents a brush that fills any object with a solid colour.
    </summary>
    """
    @property

    def Color(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the color of the brush.
    </summary>
        """
        GetDllLibPdf().PdfSolidBrush_get_Color.argtypes=[c_void_p]
        GetDllLibPdf().PdfSolidBrush_get_Color.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSolidBrush_get_Color(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @Color.setter
    def Color(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfSolidBrush_set_Color.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfSolidBrush_set_Color(self.Ptr, value.Ptr)


    def Clone(self)->'PdfBrush':
        """
    <summary>
        Creates a new copy of a brush.
    </summary>
    <returns>A new instance of the Brush class.</returns>
        """
        GetDllLibPdf().PdfSolidBrush_Clone.argtypes=[c_void_p]
        GetDllLibPdf().PdfSolidBrush_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().PdfSolidBrush_Clone(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


