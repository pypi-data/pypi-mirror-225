from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfICCColorSpace (  PdfColorSpaces) :
    """
    <summary>
        Represents an ICC based colorspace..
    </summary>
    """
    @property

    def AlternateColorSpace(self)->'PdfColorSpaces':
        """
    <summary>
        Gets or sets the alternate color space.
    </summary>
<value>The alternate color space to be used in case the one specified in the stream data is not supported.</value>
        """
        GetDllLibPdf().PdfICCColorSpace_get_AlternateColorSpace.argtypes=[c_void_p]
        GetDllLibPdf().PdfICCColorSpace_get_AlternateColorSpace.restype=c_void_p
        intPtr = GetDllLibPdf().PdfICCColorSpace_get_AlternateColorSpace(self.Ptr)
        ret = None if intPtr==None else PdfColorSpaces(intPtr)
        return ret


    @AlternateColorSpace.setter
    def AlternateColorSpace(self, value:'PdfColorSpaces'):
        GetDllLibPdf().PdfICCColorSpace_set_AlternateColorSpace.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfICCColorSpace_set_AlternateColorSpace(self.Ptr, value.Ptr)

    @property
    def ColorComponents(self)->int:
        """
    <summary>
        Gets or sets the color components.
    </summary>
<value>The number of color components in the color space described by the ICC profile data.</value>
<remarks>This number must match the number of components actually in the ICC profile. As of PDF 1.4, this value must be 1, 3 or 4.</remarks>
        """
        GetDllLibPdf().PdfICCColorSpace_get_ColorComponents.argtypes=[c_void_p]
        GetDllLibPdf().PdfICCColorSpace_get_ColorComponents.restype=c_int
        ret = GetDllLibPdf().PdfICCColorSpace_get_ColorComponents(self.Ptr)
        return ret

    @ColorComponents.setter
    def ColorComponents(self, value:int):
        GetDllLibPdf().PdfICCColorSpace_set_ColorComponents.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfICCColorSpace_set_ColorComponents(self.Ptr, value)

#    @property
#
#    def ProfileData(self)->List['Byte']:
#        """
#    <summary>
#        Gets or sets the profile data.
#    </summary>
#<value>The ICC profile data.</value>
#        """
#        GetDllLibPdf().PdfICCColorSpace_get_ProfileData.argtypes=[c_void_p]
#        GetDllLibPdf().PdfICCColorSpace_get_ProfileData.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfICCColorSpace_get_ProfileData(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, Byte)
#        return ret


#    @ProfileData.setter
#    def ProfileData(self, value:List['Byte']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().PdfICCColorSpace_set_ProfileData.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().PdfICCColorSpace_set_ProfileData(self.Ptr, vArray, vCount)


    @property

    def Range(self)->List[float]:
        """
    <summary>
        Gets or sets the range for color components. 
    </summary>
<value>An array of 2  ColorComponents numbers [ min0 max0 min1 max1 ... ] specifying the minimum and maximum valid values of the corresponding color components. These values must match the information in the ICC profile.</value>
        """
        GetDllLibPdf().PdfICCColorSpace_get_Range.argtypes=[c_void_p]
        GetDllLibPdf().PdfICCColorSpace_get_Range.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfICCColorSpace_get_Range(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_double)
        return ret

    @Range.setter
    def Range(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_double * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfICCColorSpace_set_Range.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfICCColorSpace_set_Range(self.Ptr, vArray, vCount)

#
#    def GetProfileData(self)->List['Byte']:
#        """
#    <summary>
#        Set the Color Profile.
#    </summary>
#    <returns>ICC profile data.</returns>
#        """
#        GetDllLibPdf().PdfICCColorSpace_GetProfileData.argtypes=[c_void_p]
#        GetDllLibPdf().PdfICCColorSpace_GetProfileData.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfICCColorSpace_GetProfileData(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, Byte)
#        return ret


