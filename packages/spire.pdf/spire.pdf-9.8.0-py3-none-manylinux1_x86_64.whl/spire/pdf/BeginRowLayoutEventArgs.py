from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class BeginRowLayoutEventArgs (SpireObject) :
    """
    <summary>
        Represents StartRowLayout Event arguments.
    </summary>
    """
    @property
    def RowIndex(self)->int:
        """
    <summary>
        Gets the index of the row.
    </summary>
        """
        GetDllLibPdf().BeginRowLayoutEventArgs_get_RowIndex.argtypes=[c_void_p]
        GetDllLibPdf().BeginRowLayoutEventArgs_get_RowIndex.restype=c_int
        ret = GetDllLibPdf().BeginRowLayoutEventArgs_get_RowIndex(self.Ptr)
        return ret

    @property

    def CellStyle(self)->'PdfCellStyle':
        """
    <summary>
        Gets or sets the cell style.
    </summary>
        """
        GetDllLibPdf().BeginRowLayoutEventArgs_get_CellStyle.argtypes=[c_void_p]
        GetDllLibPdf().BeginRowLayoutEventArgs_get_CellStyle.restype=c_void_p
        intPtr = GetDllLibPdf().BeginRowLayoutEventArgs_get_CellStyle(self.Ptr)
        ret = None if intPtr==None else PdfCellStyle(intPtr)
        return ret


    @CellStyle.setter
    def CellStyle(self, value:'PdfCellStyle'):
        GetDllLibPdf().BeginRowLayoutEventArgs_set_CellStyle.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().BeginRowLayoutEventArgs_set_CellStyle(self.Ptr, value.Ptr)

    @property

    def ColumnSpanMap(self)->List[int]:
        """
    <summary>
        Gets or sets the span map.
    </summary>
        """
        GetDllLibPdf().BeginRowLayoutEventArgs_get_ColumnSpanMap.argtypes=[c_void_p]
        GetDllLibPdf().BeginRowLayoutEventArgs_get_ColumnSpanMap.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().BeginRowLayoutEventArgs_get_ColumnSpanMap(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_int)
        return ret

    @ColumnSpanMap.setter
    def ColumnSpanMap(self, value:List[int]):
        vCount = len(value)
        ArrayType = c_int * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().BeginRowLayoutEventArgs_set_ColumnSpanMap.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().BeginRowLayoutEventArgs_set_ColumnSpanMap(self.Ptr, vArray, vCount)

    @property
    def Cancel(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether table drawing should stop.
    </summary>
        """
        GetDllLibPdf().BeginRowLayoutEventArgs_get_Cancel.argtypes=[c_void_p]
        GetDllLibPdf().BeginRowLayoutEventArgs_get_Cancel.restype=c_bool
        ret = GetDllLibPdf().BeginRowLayoutEventArgs_get_Cancel(self.Ptr)
        return ret

    @Cancel.setter
    def Cancel(self, value:bool):
        GetDllLibPdf().BeginRowLayoutEventArgs_set_Cancel.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().BeginRowLayoutEventArgs_set_Cancel(self.Ptr, value)

    @property
    def Skip(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this row should be ignored.
    </summary>
        """
        GetDllLibPdf().BeginRowLayoutEventArgs_get_Skip.argtypes=[c_void_p]
        GetDllLibPdf().BeginRowLayoutEventArgs_get_Skip.restype=c_bool
        ret = GetDllLibPdf().BeginRowLayoutEventArgs_get_Skip(self.Ptr)
        return ret

    @Skip.setter
    def Skip(self, value:bool):
        GetDllLibPdf().BeginRowLayoutEventArgs_set_Skip.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().BeginRowLayoutEventArgs_set_Skip(self.Ptr, value)

    @property
    def IgnoreColumnFormat(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether column string format should be ignored.
    </summary>
        """
        GetDllLibPdf().BeginRowLayoutEventArgs_get_IgnoreColumnFormat.argtypes=[c_void_p]
        GetDllLibPdf().BeginRowLayoutEventArgs_get_IgnoreColumnFormat.restype=c_bool
        ret = GetDllLibPdf().BeginRowLayoutEventArgs_get_IgnoreColumnFormat(self.Ptr)
        return ret

    @IgnoreColumnFormat.setter
    def IgnoreColumnFormat(self, value:bool):
        GetDllLibPdf().BeginRowLayoutEventArgs_set_IgnoreColumnFormat.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().BeginRowLayoutEventArgs_set_IgnoreColumnFormat(self.Ptr, value)

    @property
    def MinimalHeight(self)->float:
        """
    <summary>
        Sets the minimal height of the row.
    </summary>
        """
        GetDllLibPdf().BeginRowLayoutEventArgs_get_MinimalHeight.argtypes=[c_void_p]
        GetDllLibPdf().BeginRowLayoutEventArgs_get_MinimalHeight.restype=c_float
        ret = GetDllLibPdf().BeginRowLayoutEventArgs_get_MinimalHeight(self.Ptr)
        return ret

    @MinimalHeight.setter
    def MinimalHeight(self, value:float):
        GetDllLibPdf().BeginRowLayoutEventArgs_set_MinimalHeight.argtypes=[c_void_p, c_float]
        GetDllLibPdf().BeginRowLayoutEventArgs_set_MinimalHeight(self.Ptr, value)

