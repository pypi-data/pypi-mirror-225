from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLabColorSpace (  PdfColorSpaces) :
    """
    <summary>
        Represents a Lab colorspace
    </summary>
    """
    @property

    def BlackPoint(self)->List[float]:
        """
    <summary>
        Gets or sets BlackPoint
    </summary>
<value>An array of three numbers [XB YB ZB] specifying the tristimulus value, in the CIE 1931 XYZ space, of the diffuse black point.</value>
        """
        GetDllLibPdf().PdfLabColorSpace_get_BlackPoint.argtypes=[c_void_p]
        GetDllLibPdf().PdfLabColorSpace_get_BlackPoint.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfLabColorSpace_get_BlackPoint(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_double)
        return ret

    @BlackPoint.setter
    def BlackPoint(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_double * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfLabColorSpace_set_BlackPoint.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfLabColorSpace_set_BlackPoint(self.Ptr, vArray, vCount)

    @property

    def Range(self)->List[float]:
        """
    <summary>
        Gets or sets the Range
    </summary>
<value>An array of three numbers [XB YB ZB] specifying the tristimulus value, in the CIE 1931 XYZ space, of the diffuse black point.</value>
        """
        GetDllLibPdf().PdfLabColorSpace_get_Range.argtypes=[c_void_p]
        GetDllLibPdf().PdfLabColorSpace_get_Range.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfLabColorSpace_get_Range(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_double)
        return ret

    @Range.setter
    def Range(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_double * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfLabColorSpace_set_Range.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfLabColorSpace_set_Range(self.Ptr, vArray, vCount)

    @property

    def WhitePoint(self)->List[float]:
        """
    <summary>
        Gets or sets the white point
    </summary>
<value>An array of three numbers [XW YW ZW] specifying the tristimulus value, in the CIE 1931 XYZ space, of the diffuse white point. </value>
        """
        GetDllLibPdf().PdfLabColorSpace_get_WhitePoint.argtypes=[c_void_p]
        GetDllLibPdf().PdfLabColorSpace_get_WhitePoint.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfLabColorSpace_get_WhitePoint(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_double)
        return ret

    @WhitePoint.setter
    def WhitePoint(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_double * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfLabColorSpace_set_WhitePoint.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfLabColorSpace_set_WhitePoint(self.Ptr, vArray, vCount)

