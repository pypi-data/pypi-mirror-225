from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfButtonIconLayout (SpireObject) :
    """
    <summary>
        Represents the button icon layout options.
    </summary>
    """
    @property

    def ScaleReason(self)->'PdfButtonIconScaleReason':
        """
    <summary>
        Gets or sets the circumstances under which the icon shall be scaled inside the annotation rectangle.
    </summary>
        """
        GetDllLibPdf().PdfButtonIconLayout_get_ScaleReason.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonIconLayout_get_ScaleReason.restype=c_int
        ret = GetDllLibPdf().PdfButtonIconLayout_get_ScaleReason(self.Ptr)
        objwraped = PdfButtonIconScaleReason(ret)
        return objwraped

    @ScaleReason.setter
    def ScaleReason(self, value:'PdfButtonIconScaleReason'):
        GetDllLibPdf().PdfButtonIconLayout_set_ScaleReason.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfButtonIconLayout_set_ScaleReason(self.Ptr, value.value)

    @property

    def Spaces(self)->List[float]:
        """
    <summary>
        Gets or sets an array of two numbers between 0.0 and 1.0 indicating the fraction of leftover space to allocate at the left and bottom of the icon.
    </summary>
        """
        GetDllLibPdf().PdfButtonIconLayout_get_Spaces.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonIconLayout_get_Spaces.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfButtonIconLayout_get_Spaces(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_float)
        return ret

    @Spaces.setter
    def Spaces(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_float * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfButtonIconLayout_set_Spaces.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfButtonIconLayout_set_Spaces(self.Ptr, vArray, vCount)

    @property
    def IsFitBounds(self)->bool:
        """
    <summary>
        If true, indicates that the button appearance should be scaled to fit fully within the bounds of the annotation without taking into consideration the line width of the border.
    </summary>
        """
        GetDllLibPdf().PdfButtonIconLayout_get_IsFitBounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonIconLayout_get_IsFitBounds.restype=c_bool
        ret = GetDllLibPdf().PdfButtonIconLayout_get_IsFitBounds(self.Ptr)
        return ret

    @IsFitBounds.setter
    def IsFitBounds(self, value:bool):
        GetDllLibPdf().PdfButtonIconLayout_set_IsFitBounds.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfButtonIconLayout_set_IsFitBounds(self.Ptr, value)

    @property

    def ScaleMode(self)->'PdfButtonIconScaleMode':
        """
    <summary>
        Gets or sets the type of scaling to use.
    </summary>
        """
        GetDllLibPdf().PdfButtonIconLayout_get_ScaleMode.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonIconLayout_get_ScaleMode.restype=c_int
        ret = GetDllLibPdf().PdfButtonIconLayout_get_ScaleMode(self.Ptr)
        objwraped = PdfButtonIconScaleMode(ret)
        return objwraped

    @ScaleMode.setter
    def ScaleMode(self, value:'PdfButtonIconScaleMode'):
        GetDllLibPdf().PdfButtonIconLayout_set_ScaleMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfButtonIconLayout_set_ScaleMode(self.Ptr, value.value)

