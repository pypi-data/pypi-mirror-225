from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class LinkTargets (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def LinkTarget(self)->List['LinkTarget']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().LinkTargets_get_LinkTarget.argtypes=[c_void_p]
#        GetDllLibPdf().LinkTargets_get_LinkTarget.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().LinkTargets_get_LinkTarget(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, LinkTarget)
#        return ret


#    @LinkTarget.setter
#    def LinkTarget(self, value:List['LinkTarget']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().LinkTargets_set_LinkTarget.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().LinkTargets_set_LinkTarget(self.Ptr, vArray, vCount)


