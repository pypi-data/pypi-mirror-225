from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class StoryFragment (SpireObject) :
    """
<remarks />
    """
    @property

    def StoryBreak(self)->'Break':
        """
<remarks />
        """
        GetDllLibPdf().StoryFragment_get_StoryBreak.argtypes=[c_void_p]
        GetDllLibPdf().StoryFragment_get_StoryBreak.restype=c_void_p
        intPtr = GetDllLibPdf().StoryFragment_get_StoryBreak(self.Ptr)
        ret = None if intPtr==None else Break(intPtr)
        return ret


    @StoryBreak.setter
    def StoryBreak(self, value:'Break'):
        GetDllLibPdf().StoryFragment_set_StoryBreak.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().StoryFragment_set_StoryBreak(self.Ptr, value.Ptr)

    @property

    def Items(self)->List['SpireObject']:
        """
<remarks />
        """
        GetDllLibPdf().StoryFragment_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().StoryFragment_get_Items.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().StoryFragment_get_Items(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, SpireObject)
        return ret

    @Items.setter
    def Items(self, value:List['SpireObject']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().StoryFragment_set_Items.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().StoryFragment_set_Items(self.Ptr, vArray, vCount)

    @property

    def StoryBreak1(self)->'Break':
        """
<remarks />
        """
        GetDllLibPdf().StoryFragment_get_StoryBreak1.argtypes=[c_void_p]
        GetDllLibPdf().StoryFragment_get_StoryBreak1.restype=c_void_p
        intPtr = GetDllLibPdf().StoryFragment_get_StoryBreak1(self.Ptr)
        ret = None if intPtr==None else Break(intPtr)
        return ret


    @StoryBreak1.setter
    def StoryBreak1(self, value:'Break'):
        GetDllLibPdf().StoryFragment_set_StoryBreak1.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().StoryFragment_set_StoryBreak1(self.Ptr, value.Ptr)

    @property

    def StoryName(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().StoryFragment_get_StoryName.argtypes=[c_void_p]
        GetDllLibPdf().StoryFragment_get_StoryName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().StoryFragment_get_StoryName(self.Ptr))
        return ret


    @StoryName.setter
    def StoryName(self, value:str):
        GetDllLibPdf().StoryFragment_set_StoryName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().StoryFragment_set_StoryName(self.Ptr, value)

    @property

    def FragmentName(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().StoryFragment_get_FragmentName.argtypes=[c_void_p]
        GetDllLibPdf().StoryFragment_get_FragmentName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().StoryFragment_get_FragmentName(self.Ptr))
        return ret


    @FragmentName.setter
    def FragmentName(self, value:str):
        GetDllLibPdf().StoryFragment_set_FragmentName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().StoryFragment_set_FragmentName(self.Ptr, value)

    @property

    def FragmentType(self)->'FragmentType':
        """
<remarks />
        """
        GetDllLibPdf().StoryFragment_get_FragmentType.argtypes=[c_void_p]
        GetDllLibPdf().StoryFragment_get_FragmentType.restype=c_int
        ret = GetDllLibPdf().StoryFragment_get_FragmentType(self.Ptr)
        objwraped = FragmentType(ret)
        return objwraped

    @FragmentType.setter
    def FragmentType(self, value:'FragmentType'):
        GetDllLibPdf().StoryFragment_set_FragmentType.argtypes=[c_void_p, c_int]
        GetDllLibPdf().StoryFragment_set_FragmentType(self.Ptr, value.value)

