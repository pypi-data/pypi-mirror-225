from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class TableCell (SpireObject) :
    """
<remarks />
    """
    @property

    def Items(self)->List['SpireObject']:
        """
<remarks />
        """
        GetDllLibPdf().TableCell_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().TableCell_get_Items.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().TableCell_get_Items(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, SpireObject)
        return ret

    @Items.setter
    def Items(self, value:List['SpireObject']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().TableCell_set_Items.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().TableCell_set_Items(self.Ptr, vArray, vCount)

#    @property
#
#    def ItemsElementName(self)->List['ItemsChoiceType']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().TableCell_get_ItemsElementName.argtypes=[c_void_p]
#        GetDllLibPdf().TableCell_get_ItemsElementName.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().TableCell_get_ItemsElementName(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, ItemsChoiceType)
#        return ret


#    @ItemsElementName.setter
#    def ItemsElementName(self, value:List['ItemsChoiceType']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().TableCell_set_ItemsElementName.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().TableCell_set_ItemsElementName(self.Ptr, vArray, vCount)


    @property
    def RowSpan(self)->int:
        """
<remarks />
        """
        GetDllLibPdf().TableCell_get_RowSpan.argtypes=[c_void_p]
        GetDllLibPdf().TableCell_get_RowSpan.restype=c_int
        ret = GetDllLibPdf().TableCell_get_RowSpan(self.Ptr)
        return ret

    @RowSpan.setter
    def RowSpan(self, value:int):
        GetDllLibPdf().TableCell_set_RowSpan.argtypes=[c_void_p, c_int]
        GetDllLibPdf().TableCell_set_RowSpan(self.Ptr, value)

    @property
    def ColumnSpan(self)->int:
        """
<remarks />
        """
        GetDllLibPdf().TableCell_get_ColumnSpan.argtypes=[c_void_p]
        GetDllLibPdf().TableCell_get_ColumnSpan.restype=c_int
        ret = GetDllLibPdf().TableCell_get_ColumnSpan(self.Ptr)
        return ret

    @ColumnSpan.setter
    def ColumnSpan(self, value:int):
        GetDllLibPdf().TableCell_set_ColumnSpan.argtypes=[c_void_p, c_int]
        GetDllLibPdf().TableCell_set_ColumnSpan(self.Ptr, value)

