from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAnnotationBorder (SpireObject) :
    @dispatch
    def __init__(self,borderWidth:float):

        GetDllLibPdf().PdfAnnotationBorder_CreatePdfAnnotationBorderB.argtypes=[c_float]
        GetDllLibPdf().PdfAnnotationBorder_CreatePdfAnnotationBorderB.restype = c_void_p
        intPtr = GetDllLibPdf().PdfAnnotationBorder_CreatePdfAnnotationBorderB(borderWidth)
        super(PdfAnnotationBorder, self).__init__(intPtr)

    @dispatch
    def __init__(self,borderWidth:float, horizontalRadius:float, verticalRadius:float):

        GetDllLibPdf().PdfAnnotationBorder_CreatePdfAnnotationBorderBHV.argtypes=[c_float,c_float,c_float]
        GetDllLibPdf().PdfAnnotationBorder_CreatePdfAnnotationBorderBHV.restype = c_void_p
        intPtr = GetDllLibPdf().PdfAnnotationBorder_CreatePdfAnnotationBorderBHV(borderWidth,horizontalRadius,verticalRadius)
        super(PdfAnnotationBorder, self).__init__(intPtr)
    """
    <summary>
        Represents the appearance of an annotation's border.
    </summary>
    """
    @property
    def HorizontalRadius(self)->float:
        """
    <summary>
        Gets or sets a horizontal corner radius.
    </summary>
        """
        GetDllLibPdf().PdfAnnotationBorder_get_HorizontalRadius.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotationBorder_get_HorizontalRadius.restype=c_float
        ret = GetDllLibPdf().PdfAnnotationBorder_get_HorizontalRadius(self.Ptr)
        return ret

    @HorizontalRadius.setter
    def HorizontalRadius(self, value:float):
        GetDllLibPdf().PdfAnnotationBorder_set_HorizontalRadius.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfAnnotationBorder_set_HorizontalRadius(self.Ptr, value)

    @property
    def VerticalRadius(self)->float:
        """
    <summary>
        Gets or sets a vertical corner radius.
    </summary>
        """
        GetDllLibPdf().PdfAnnotationBorder_get_VerticalRadius.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotationBorder_get_VerticalRadius.restype=c_float
        ret = GetDllLibPdf().PdfAnnotationBorder_get_VerticalRadius(self.Ptr)
        return ret

    @VerticalRadius.setter
    def VerticalRadius(self, value:float):
        GetDllLibPdf().PdfAnnotationBorder_set_VerticalRadius.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfAnnotationBorder_set_VerticalRadius(self.Ptr, value)

    @property
    def Width(self)->float:
        """
    <summary>
        Gets or sets the width of annotation's border. 
    </summary>
<value>A float value specifying the width of the annotation's border. </value>
        """
        GetDllLibPdf().PdfAnnotationBorder_get_Width.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotationBorder_get_Width.restype=c_float
        ret = GetDllLibPdf().PdfAnnotationBorder_get_Width(self.Ptr)
        return ret

    @Width.setter
    def Width(self, value:float):
        GetDllLibPdf().PdfAnnotationBorder_set_Width.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfAnnotationBorder_set_Width(self.Ptr, value)

