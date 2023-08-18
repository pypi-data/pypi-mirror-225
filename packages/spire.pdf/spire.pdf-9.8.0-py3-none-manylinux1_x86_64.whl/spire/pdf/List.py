from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfList (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def Items(self)->List['ListItem']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().List_get_Items.argtypes=[c_void_p]
#        GetDllLibPdf().List_get_Items.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().List_get_Items(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, ListItem)
#        return ret


#    @Items.setter
#    def Items(self, value:List['ListItem']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().List_set_Items.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().List_set_Items(self.Ptr, vArray, vCount)


