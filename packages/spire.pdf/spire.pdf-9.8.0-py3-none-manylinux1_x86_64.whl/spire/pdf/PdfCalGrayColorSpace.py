from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCalGrayColorSpace (  PdfColorSpaces) :
    """
    <summary>
        Represents a CalGray colorspace.
    </summary>
    """
    @property

    def BlackPoint(self)->List[float]:
        """
    <summary>
        Gets or sets the black point. 
    </summary>
<value>An array of three numbers [XB YB ZB] specifying the tristimulus value, in the CIE 1931 XYZ space, of the diffuse black point. Default value: [ 0.0 0.0 0.0 ].</value>
        """
        GetDllLibPdf().PdfCalGrayColorSpace_get_BlackPoint.argtypes=[c_void_p]
        GetDllLibPdf().PdfCalGrayColorSpace_get_BlackPoint.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfCalGrayColorSpace_get_BlackPoint(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_double)
        return ret

    @BlackPoint.setter
    def BlackPoint(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_double * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfCalGrayColorSpace_set_BlackPoint.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfCalGrayColorSpace_set_BlackPoint(self.Ptr, vArray, vCount)

    @property
    def Gamma(self)->float:
        """
    <summary>
        Gets or sets the gamma.
    </summary>
        """
        GetDllLibPdf().PdfCalGrayColorSpace_get_Gamma.argtypes=[c_void_p]
        GetDllLibPdf().PdfCalGrayColorSpace_get_Gamma.restype=c_double
        ret = GetDllLibPdf().PdfCalGrayColorSpace_get_Gamma(self.Ptr)
        return ret

    @Gamma.setter
    def Gamma(self, value:float):
        GetDllLibPdf().PdfCalGrayColorSpace_set_Gamma.argtypes=[c_void_p, c_double]
        GetDllLibPdf().PdfCalGrayColorSpace_set_Gamma(self.Ptr, value)

    @property

    def WhitePoint(self)->List[float]:
        """
    <summary>
        Gets or sets the white point.
    </summary>
<value>An array of three numbers [XW YW ZW] specifying the tristimulus value, in the CIE 1931 XYZ space, of the diffuse white point. The numbers XW and ZW must be positive, and YW must be equal to 1.0.</value>
        """
        GetDllLibPdf().PdfCalGrayColorSpace_get_WhitePoint.argtypes=[c_void_p]
        GetDllLibPdf().PdfCalGrayColorSpace_get_WhitePoint.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfCalGrayColorSpace_get_WhitePoint(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_double)
        return ret

    @WhitePoint.setter
    def WhitePoint(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_double * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfCalGrayColorSpace_set_WhitePoint.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfCalGrayColorSpace_set_WhitePoint(self.Ptr, vArray, vCount)

