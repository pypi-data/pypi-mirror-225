from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class QueryNextRowEventArgs (SpireObject) :
    """
    <summary>
        Represents arguments of the NextRow Event.
    </summary>
    """
    @property

    def RowData(self)->List[str]:
        """
    <summary>
        Gets or sets the row data.
    </summary>
        """
        GetDllLibPdf().QueryNextRowEventArgs_get_RowData.argtypes=[c_void_p]
        GetDllLibPdf().QueryNextRowEventArgs_get_RowData.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().QueryNextRowEventArgs_get_RowData(self.Ptr)
        ret = GetStrVectorFromArray(intPtrArray, c_void_p)
        return ret

    @RowData.setter
    def RowData(self, value:List[str]):
        vCount = len(value)
        ArrayType = c_wchar_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().QueryNextRowEventArgs_set_RowData.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().QueryNextRowEventArgs_set_RowData(self.Ptr, vArray, vCount)

    @property
    def ColumnCount(self)->int:
        """
    <summary>
        Gets the column count.
    </summary>
        """
        GetDllLibPdf().QueryNextRowEventArgs_get_ColumnCount.argtypes=[c_void_p]
        GetDllLibPdf().QueryNextRowEventArgs_get_ColumnCount.restype=c_int
        ret = GetDllLibPdf().QueryNextRowEventArgs_get_ColumnCount(self.Ptr)
        return ret

    @property
    def RowIndex(self)->int:
        """
    <summary>
        Gets the index of the row.
    </summary>
        """
        GetDllLibPdf().QueryNextRowEventArgs_get_RowIndex.argtypes=[c_void_p]
        GetDllLibPdf().QueryNextRowEventArgs_get_RowIndex.restype=c_int
        ret = GetDllLibPdf().QueryNextRowEventArgs_get_RowIndex(self.Ptr)
        return ret

