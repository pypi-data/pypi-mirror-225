from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class TableRowGroup (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def Items(self)->List['TableRow']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().TableRowGroup_get_Items.argtypes=[c_void_p]
#        GetDllLibPdf().TableRowGroup_get_Items.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().TableRowGroup_get_Items(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, TableRow)
#        return ret


#    @Items.setter
#    def Items(self, value:List['TableRow']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().TableRowGroup_set_Items.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().TableRowGroup_set_Items(self.Ptr, vArray, vCount)


