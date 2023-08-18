from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCalRGBColorSpace (  PdfColorSpaces) :
    """
    <summary>
        Representing a CalRGB colorspace. 
    </summary>
    """
    @property

    def BlackPoint(self)->List[float]:
        """
    <summary>
        Gets or sets the black point. 
    </summary>
<value>An array of three numbers [XB YB ZB] specifying the tristimulus value, in the CIE 1931 XYZ space, of the diffuse black point. </value>
        """
        GetDllLibPdf().PdfCalRGBColorSpace_get_BlackPoint.argtypes=[c_void_p]
        GetDllLibPdf().PdfCalRGBColorSpace_get_BlackPoint.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfCalRGBColorSpace_get_BlackPoint(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_double)
        return ret

    @BlackPoint.setter
    def BlackPoint(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_double * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfCalRGBColorSpace_set_BlackPoint.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfCalRGBColorSpace_set_BlackPoint(self.Ptr, vArray, vCount)

    @property

    def Gamma(self)->List[float]:
        """
    <summary>
        Gets or sets the gamma. 
    </summary>
<value>An array of three numbers [GR GG GB] specifying the gamma for the red, green, and blue components of the color space. </value>
        """
        GetDllLibPdf().PdfCalRGBColorSpace_get_Gamma.argtypes=[c_void_p]
        GetDllLibPdf().PdfCalRGBColorSpace_get_Gamma.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfCalRGBColorSpace_get_Gamma(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_double)
        return ret

    @Gamma.setter
    def Gamma(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_double * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfCalRGBColorSpace_set_Gamma.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfCalRGBColorSpace_set_Gamma(self.Ptr, vArray, vCount)

    @property

    def Matrix(self)->List[float]:
        """
    <summary>
        Gets or sets the colorspace transformation matrix. 
    </summary>
<value>An array of nine numbers [XA YA ZA XB YB ZB XC YC ZC] specifying the linear interpretation of the decoded A, B, and C components of the color space with respect to the final XYZ representation.</value>
        """
        GetDllLibPdf().PdfCalRGBColorSpace_get_Matrix.argtypes=[c_void_p]
        GetDllLibPdf().PdfCalRGBColorSpace_get_Matrix.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfCalRGBColorSpace_get_Matrix(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_double)
        return ret

    @Matrix.setter
    def Matrix(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_double * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfCalRGBColorSpace_set_Matrix.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfCalRGBColorSpace_set_Matrix(self.Ptr, vArray, vCount)

    @property

    def WhitePoint(self)->List[float]:
        """
    <summary>
        Gets or sets the white point.
    </summary>
<value>An array of three numbers [XW YW ZW] specifying the tristimulus value, in the CIE 1931 XYZ space, of the diffuse white point.</value>
        """
        GetDllLibPdf().PdfCalRGBColorSpace_get_WhitePoint.argtypes=[c_void_p]
        GetDllLibPdf().PdfCalRGBColorSpace_get_WhitePoint.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfCalRGBColorSpace_get_WhitePoint(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_double)
        return ret

    @WhitePoint.setter
    def WhitePoint(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_double * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfCalRGBColorSpace_set_WhitePoint.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfCalRGBColorSpace_set_WhitePoint(self.Ptr, vArray, vCount)

