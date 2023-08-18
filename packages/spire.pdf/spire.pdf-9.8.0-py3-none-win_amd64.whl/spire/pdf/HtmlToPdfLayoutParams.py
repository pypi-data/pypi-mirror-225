from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class HtmlToPdfLayoutParams (  PdfLayoutParams) :
    """
    <summary>
        Represents the layout parameters.
    </summary>
    """
    @property

    def Page(self)->'PdfPageBase':
        """
    <summary>
        Gets or sets the starting layout page.
    </summary>
        """
        GetDllLibPdf().HtmlToPdfLayoutParams_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().HtmlToPdfLayoutParams_get_Page.restype=c_void_p
        intPtr = GetDllLibPdf().HtmlToPdfLayoutParams_get_Page(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @Page.setter
    def Page(self, value:'PdfPageBase'):
        GetDllLibPdf().HtmlToPdfLayoutParams_set_Page.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().HtmlToPdfLayoutParams_set_Page(self.Ptr, value.Ptr)

    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets or sets the lay outing bounds.
    </summary>
        """
        GetDllLibPdf().HtmlToPdfLayoutParams_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().HtmlToPdfLayoutParams_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().HtmlToPdfLayoutParams_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Bounds.setter
    def Bounds(self, value:'RectangleF'):
        GetDllLibPdf().HtmlToPdfLayoutParams_set_Bounds.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().HtmlToPdfLayoutParams_set_Bounds(self.Ptr, value.Ptr)

    @property

    def VerticalOffsets(self)->List[float]:
        """
    <summary>
        Gets or sets the vertical offsets.
    </summary>
<value>The vertical offsets.</value>
        """
        GetDllLibPdf().HtmlToPdfLayoutParams_get_VerticalOffsets.argtypes=[c_void_p]
        GetDllLibPdf().HtmlToPdfLayoutParams_get_VerticalOffsets.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().HtmlToPdfLayoutParams_get_VerticalOffsets(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_float)
        return ret

    @VerticalOffsets.setter
    def VerticalOffsets(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_float * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().HtmlToPdfLayoutParams_set_VerticalOffsets.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().HtmlToPdfLayoutParams_set_VerticalOffsets(self.Ptr, vArray, vCount)

    @property

    def Format(self)->'PdfTextLayout':
        """
    <summary>
        Gets or sets the lay outing settings.
    </summary>
        """
        GetDllLibPdf().HtmlToPdfLayoutParams_get_Format.argtypes=[c_void_p]
        GetDllLibPdf().HtmlToPdfLayoutParams_get_Format.restype=c_void_p
        intPtr = GetDllLibPdf().HtmlToPdfLayoutParams_get_Format(self.Ptr)
        ret = None if intPtr==None else PdfTextLayout(intPtr)
        return ret


    @Format.setter
    def Format(self, value:'PdfTextLayout'):
        GetDllLibPdf().HtmlToPdfLayoutParams_set_Format.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().HtmlToPdfLayoutParams_set_Format(self.Ptr, value.Ptr)

