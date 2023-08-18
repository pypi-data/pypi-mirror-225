from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class DiscardControl (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def Discard(self)->List['Discard']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().DiscardControl_get_Discard.argtypes=[c_void_p]
#        GetDllLibPdf().DiscardControl_get_Discard.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().DiscardControl_get_Discard(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, Discard)
#        return ret


#    @Discard.setter
#    def Discard(self, value:List['Discard']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().DiscardControl_set_Discard.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().DiscardControl_set_Discard(self.Ptr, vArray, vCount)


