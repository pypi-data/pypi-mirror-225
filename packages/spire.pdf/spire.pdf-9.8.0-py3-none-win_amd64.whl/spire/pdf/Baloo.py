from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Baloo (SpireObject) :
    """

    """
    @property

    def Requires(self)->str:
        """

        """
        GetDllLibPdf().Baloo_get_Requires.argtypes=[c_void_p]
        GetDllLibPdf().Baloo_get_Requires.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Baloo_get_Requires(self.Ptr))
        return ret


    @Requires.setter
    def Requires(self, value:str):
        GetDllLibPdf().Baloo_set_Requires.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Baloo_set_Requires(self.Ptr, value)

    @property

    def Items(self)->List['SpireObject']:
        """
<remarks />
        """
        GetDllLibPdf().Baloo_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().Baloo_get_Items.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().Baloo_get_Items(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, SpireObject)
        return ret

    @Items.setter
    def Items(self, value:List['SpireObject']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().Baloo_set_Items.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().Baloo_set_Items(self.Ptr, vArray, vCount)

