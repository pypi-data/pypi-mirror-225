from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class CellLayoutEventArgs (SpireObject) :
    """
    <summary>
        The base class for cell layout arguments.
    </summary>
    """
    @property
    def RowIndex(self)->int:
        """
    <summary>
        Gets the index of the row.
    </summary>
        """
        GetDllLibPdf().CellLayoutEventArgs_get_RowIndex.argtypes=[c_void_p]
        GetDllLibPdf().CellLayoutEventArgs_get_RowIndex.restype=c_int
        ret = GetDllLibPdf().CellLayoutEventArgs_get_RowIndex(self.Ptr)
        return ret

    @property
    def CellIndex(self)->int:
        """
    <summary>
        Gets the index of the cell.
    </summary>
        """
        GetDllLibPdf().CellLayoutEventArgs_get_CellIndex.argtypes=[c_void_p]
        GetDllLibPdf().CellLayoutEventArgs_get_CellIndex.restype=c_int
        ret = GetDllLibPdf().CellLayoutEventArgs_get_CellIndex(self.Ptr)
        return ret

    @property

    def Value(self)->str:
        """
    <summary>
        Gets the value.
    </summary>
<remarks>The value might be null or an empty string,
            which means that either no text were acquired or all
            text was on the previous page.</remarks>
        """
        GetDllLibPdf().CellLayoutEventArgs_get_Value.argtypes=[c_void_p]
        GetDllLibPdf().CellLayoutEventArgs_get_Value.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().CellLayoutEventArgs_get_Value(self.Ptr))
        return ret


    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets the bounds of the cell.
    </summary>
        """
        GetDllLibPdf().CellLayoutEventArgs_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().CellLayoutEventArgs_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().CellLayoutEventArgs_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @property

    def Graphics(self)->'PdfCanvas':
        """
    <summary>
        Gets the graphics, on which the cell should be drawn.
    </summary>
        """
        GetDllLibPdf().CellLayoutEventArgs_get_Graphics.argtypes=[c_void_p]
        GetDllLibPdf().CellLayoutEventArgs_get_Graphics.restype=c_void_p
        intPtr = GetDllLibPdf().CellLayoutEventArgs_get_Graphics(self.Ptr)
        ret = None if intPtr==None else PdfCanvas(intPtr)
        return ret


