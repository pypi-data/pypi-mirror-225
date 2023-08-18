from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Story (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def StoryFragmentReference(self)->List['StoryFragmentReference']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().Story_get_StoryFragmentReference.argtypes=[c_void_p]
#        GetDllLibPdf().Story_get_StoryFragmentReference.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().Story_get_StoryFragmentReference(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, StoryFragmentReference)
#        return ret


#    @StoryFragmentReference.setter
#    def StoryFragmentReference(self, value:List['StoryFragmentReference']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().Story_set_StoryFragmentReference.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().Story_set_StoryFragmentReference(self.Ptr, vArray, vCount)


    @property

    def StoryName(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Story_get_StoryName.argtypes=[c_void_p]
        GetDllLibPdf().Story_get_StoryName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Story_get_StoryName(self.Ptr))
        return ret


    @StoryName.setter
    def StoryName(self, value:str):
        GetDllLibPdf().Story_set_StoryName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Story_set_StoryName(self.Ptr, value)

