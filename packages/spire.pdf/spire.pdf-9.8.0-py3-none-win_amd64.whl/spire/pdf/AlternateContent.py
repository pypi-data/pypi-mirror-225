from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class AlternateContent (SpireObject) :
    """

    """
    @property
    def Ignorable(self)->bool:
        """

        """
        GetDllLibPdf().AlternateContent_get_Ignorable.argtypes=[c_void_p]
        GetDllLibPdf().AlternateContent_get_Ignorable.restype=c_bool
        ret = GetDllLibPdf().AlternateContent_get_Ignorable(self.Ptr)
        return ret

    @Ignorable.setter
    def Ignorable(self, value:bool):
        GetDllLibPdf().AlternateContent_set_Ignorable.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().AlternateContent_set_Ignorable(self.Ptr, value)

    @property

    def Items(self)->List['SpireObject']:
        """
<remarks />
        """
        GetDllLibPdf().AlternateContent_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().AlternateContent_get_Items.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().AlternateContent_get_Items(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, SpireObject)
        return ret

    @Items.setter
    def Items(self, value:List['SpireObject']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().AlternateContent_set_Items.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().AlternateContent_set_Items(self.Ptr, vArray, vCount)

