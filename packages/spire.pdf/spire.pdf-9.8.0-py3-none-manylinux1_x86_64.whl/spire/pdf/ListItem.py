from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ListItem (SpireObject) :
    """
<remarks />
    """
    @property

    def Items(self)->List['SpireObject']:
        """
<remarks />
        """
        GetDllLibPdf().ListItem_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().ListItem_get_Items.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().ListItem_get_Items(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, SpireObject)
        return ret

    @Items.setter
    def Items(self, value:List['SpireObject']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().ListItem_set_Items.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().ListItem_set_Items(self.Ptr, vArray, vCount)

    @property

    def Marker(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().ListItem_get_Marker.argtypes=[c_void_p]
        GetDllLibPdf().ListItem_get_Marker.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().ListItem_get_Marker(self.Ptr))
        return ret


    @Marker.setter
    def Marker(self, value:str):
        GetDllLibPdf().ListItem_set_Marker.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().ListItem_set_Marker(self.Ptr, value)

