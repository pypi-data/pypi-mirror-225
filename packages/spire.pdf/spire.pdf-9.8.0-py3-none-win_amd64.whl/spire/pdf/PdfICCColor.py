from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfICCColor (  PdfComplexColor) :
    """
    <summary>
        Represents an ICC color, based on an ICC colorspace.
    </summary>
    """
    @property

    def ColorComponents(self)->List[float]:
        """
    <summary>
        Gets or sets the color components. 
    </summary>
<value>An array of values that describe the color in the ICC colorspace. </value>
<remarks>The length of this array must match the value of ColorComponents property on the underlying ICC colorspace. </remarks>
        """
        GetDllLibPdf().PdfICCColor_get_ColorComponents.argtypes=[c_void_p]
        GetDllLibPdf().PdfICCColor_get_ColorComponents.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfICCColor_get_ColorComponents(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_double)
        return ret

    @ColorComponents.setter
    def ColorComponents(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_double * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfICCColor_set_ColorComponents.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfICCColor_set_ColorComponents(self.Ptr, vArray, vCount)

