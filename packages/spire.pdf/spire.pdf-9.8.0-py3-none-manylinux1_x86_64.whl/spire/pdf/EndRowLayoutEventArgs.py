from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class EndRowLayoutEventArgs (SpireObject) :
    """
    <summary>
        Represents arguments of EndRowLayoutEvent.
    </summary>
    """
    @property
    def RowIndex(self)->int:
        """
    <summary>
        Gets the index of the row.
    </summary>
        """
        GetDllLibPdf().EndRowLayoutEventArgs_get_RowIndex.argtypes=[c_void_p]
        GetDllLibPdf().EndRowLayoutEventArgs_get_RowIndex.restype=c_int
        ret = GetDllLibPdf().EndRowLayoutEventArgs_get_RowIndex(self.Ptr)
        return ret

    @property
    def LayoutCompleted(self)->bool:
        """
    <summary>
        Gets a value indicating whether the row was drawn completely
            (nothing should be printed on the next page).
    </summary>
        """
        GetDllLibPdf().EndRowLayoutEventArgs_get_LayoutCompleted.argtypes=[c_void_p]
        GetDllLibPdf().EndRowLayoutEventArgs_get_LayoutCompleted.restype=c_bool
        ret = GetDllLibPdf().EndRowLayoutEventArgs_get_LayoutCompleted(self.Ptr)
        return ret

    @property
    def Cancel(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this row should be the last one printed.
    </summary>
        """
        GetDllLibPdf().EndRowLayoutEventArgs_get_Cancel.argtypes=[c_void_p]
        GetDllLibPdf().EndRowLayoutEventArgs_get_Cancel.restype=c_bool
        ret = GetDllLibPdf().EndRowLayoutEventArgs_get_Cancel(self.Ptr)
        return ret

    @Cancel.setter
    def Cancel(self, value:bool):
        GetDllLibPdf().EndRowLayoutEventArgs_set_Cancel.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().EndRowLayoutEventArgs_set_Cancel(self.Ptr, value)

    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets or sets the row bounds.
    </summary>
        """
        GetDllLibPdf().EndRowLayoutEventArgs_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().EndRowLayoutEventArgs_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().EndRowLayoutEventArgs_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


