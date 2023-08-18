from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfKnownColorSpace (  PdfColorSpaces) :
    """
    <summary>
        Represents an indexed colorspace.
    </summary>
    """
    @property

    def BaseColorSpace(self)->'PdfColorSpaces':
        """
    <summary>
        Gets or sets the base colorspace. 
    </summary>
<value>The color space in which the values in the color table are to be interpreted.</value>
        """
        GetDllLibPdf().PdfKnownColorSpace_get_BaseColorSpace.argtypes=[c_void_p]
        GetDllLibPdf().PdfKnownColorSpace_get_BaseColorSpace.restype=c_void_p
        intPtr = GetDllLibPdf().PdfKnownColorSpace_get_BaseColorSpace(self.Ptr)
        ret = None if intPtr==None else PdfColorSpaces(intPtr)
        return ret


    @BaseColorSpace.setter
    def BaseColorSpace(self, value:'PdfColorSpaces'):
        GetDllLibPdf().PdfKnownColorSpace_set_BaseColorSpace.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfKnownColorSpace_set_BaseColorSpace(self.Ptr, value.Ptr)

    @property
    def MaxColorIndex(self)->int:
        """
    <summary>
        Gets or sets the index of the max color.
    </summary>
<value>The maximum index that can be used to access the values in the color table.</value>
        """
        GetDllLibPdf().PdfKnownColorSpace_get_MaxColorIndex.argtypes=[c_void_p]
        GetDllLibPdf().PdfKnownColorSpace_get_MaxColorIndex.restype=c_int
        ret = GetDllLibPdf().PdfKnownColorSpace_get_MaxColorIndex(self.Ptr)
        return ret

    @MaxColorIndex.setter
    def MaxColorIndex(self, value:int):
        GetDllLibPdf().PdfKnownColorSpace_set_MaxColorIndex.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfKnownColorSpace_set_MaxColorIndex(self.Ptr, value)

#    @property
#
#    def IndexedColorTable(self)->List['Byte']:
#        """
#    <summary>
#        Gets or sets the color table. 
#    </summary>
#<value>The table of color components.</value>
#<remarks>The color table data must be m * (maxIndex + 1) bytes long, where m is the number of color components in the base color space. Each byte is an unsigned integer in the range 0 to 255 that is scaled to the range of the corresponding color component in the base color space; that is, 0 corresponds to the minimum value in the range for that component, and 255 corresponds to the maximum.</remarks>
#        """
#        GetDllLibPdf().PdfKnownColorSpace_get_IndexedColorTable.argtypes=[c_void_p]
#        GetDllLibPdf().PdfKnownColorSpace_get_IndexedColorTable.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfKnownColorSpace_get_IndexedColorTable(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, Byte)
#        return ret


#    @IndexedColorTable.setter
#    def IndexedColorTable(self, value:List['Byte']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().PdfKnownColorSpace_set_IndexedColorTable.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().PdfKnownColorSpace_set_IndexedColorTable(self.Ptr, vArray, vCount)


#
#    def GetProfileData(self)->List['Byte']:
#        """
#    <summary>
#        Gets the profile data.
#    </summary>
#    <returns>The profile data.</returns>
#        """
#        GetDllLibPdf().PdfKnownColorSpace_GetProfileData.argtypes=[c_void_p]
#        GetDllLibPdf().PdfKnownColorSpace_GetProfileData.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PdfKnownColorSpace_GetProfileData(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, Byte)
#        return ret


