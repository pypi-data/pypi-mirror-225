from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class StoryFragments (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def StoryFragment(self)->List['StoryFragment']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().StoryFragments_get_StoryFragment.argtypes=[c_void_p]
#        GetDllLibPdf().StoryFragments_get_StoryFragment.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().StoryFragments_get_StoryFragment(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, StoryFragment)
#        return ret


#    @StoryFragment.setter
#    def StoryFragment(self, value:List['StoryFragment']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().StoryFragments_set_StoryFragment.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().StoryFragments_set_StoryFragment(self.Ptr, vArray, vCount)


