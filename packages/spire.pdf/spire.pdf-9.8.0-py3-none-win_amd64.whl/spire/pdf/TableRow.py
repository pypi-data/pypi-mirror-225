from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class TableRow (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def Items(self)->List['TableCell']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().TableRow_get_Items.argtypes=[c_void_p]
#        GetDllLibPdf().TableRow_get_Items.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().TableRow_get_Items(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, TableCell)
#        return ret


#    @Items.setter
#    def Items(self, value:List['TableCell']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().TableRow_set_Items.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().TableRow_set_Items(self.Ptr, vArray, vCount)


