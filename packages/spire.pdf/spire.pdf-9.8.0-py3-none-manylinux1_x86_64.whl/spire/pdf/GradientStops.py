from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class GradientStops (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def GradientStop(self)->List['GradientStop']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().GradientStops_get_GradientStop.argtypes=[c_void_p]
#        GetDllLibPdf().GradientStops_get_GradientStop.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().GradientStops_get_GradientStop(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, GradientStop)
#        return ret


#    @GradientStop.setter
#    def GradientStop(self, value:List['GradientStop']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().GradientStops_set_GradientStop.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().GradientStops_set_GradientStop(self.Ptr, vArray, vCount)


