from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ResourceDictionary (SpireObject) :
    """
<remarks />
    """
    @property

    def Items(self)->List['SpireObject']:
        """
<remarks />
        """
        GetDllLibPdf().ResourceDictionary_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().ResourceDictionary_get_Items.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().ResourceDictionary_get_Items(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, SpireObject)
        return ret

    @Items.setter
    def Items(self, value:List['SpireObject']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().ResourceDictionary_set_Items.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().ResourceDictionary_set_Items(self.Ptr, vArray, vCount)

    @property

    def Source(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().ResourceDictionary_get_Source.argtypes=[c_void_p]
        GetDllLibPdf().ResourceDictionary_get_Source.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().ResourceDictionary_get_Source(self.Ptr))
        return ret


    @Source.setter
    def Source(self, value:str):
        GetDllLibPdf().ResourceDictionary_set_Source.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().ResourceDictionary_set_Source(self.Ptr, value)

