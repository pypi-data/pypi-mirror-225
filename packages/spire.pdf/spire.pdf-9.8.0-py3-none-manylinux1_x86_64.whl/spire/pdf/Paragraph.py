from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Paragraph (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def Items(self)->List['NamedElement']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().Paragraph_get_Items.argtypes=[c_void_p]
#        GetDllLibPdf().Paragraph_get_Items.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().Paragraph_get_Items(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, NamedElement)
#        return ret


#    @Items.setter
#    def Items(self, value:List['NamedElement']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().Paragraph_set_Items.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().Paragraph_set_Items(self.Ptr, vArray, vCount)


