from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Fallback (SpireObject) :
    """

    """
    @property

    def Items(self)->List['SpireObject']:
        """
<remarks />
        """
        GetDllLibPdf().Fallback_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().Fallback_get_Items.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().Fallback_get_Items(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, SpireObject)
        return ret

    @Items.setter
    def Items(self, value:List['SpireObject']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().Fallback_set_Items.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().Fallback_set_Items(self.Ptr, vArray, vCount)

