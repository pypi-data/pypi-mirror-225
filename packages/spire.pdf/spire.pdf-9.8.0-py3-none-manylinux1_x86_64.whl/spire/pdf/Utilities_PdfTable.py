from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Utilities_PdfTable (SpireObject) :
    """
    <summary>
        define a pdf table
    </summary>
    """
    def GetRowCount(self)->int:
        """
    <summary>
        Get the current table row count
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().Utilities_PdfTable_GetRowCount.argtypes=[c_void_p]
        GetDllLibPdf().Utilities_PdfTable_GetRowCount.restype=c_int
        ret = GetDllLibPdf().Utilities_PdfTable_GetRowCount(self.Ptr)
        return ret

    def GetColumnCount(self)->int:
        """
    <summary>
        Get the current table column count
    </summary>
    <returns></returns>
        """
        GetDllLibPdf().Utilities_PdfTable_GetColumnCount.argtypes=[c_void_p]
        GetDllLibPdf().Utilities_PdfTable_GetColumnCount.restype=c_int
        ret = GetDllLibPdf().Utilities_PdfTable_GetColumnCount(self.Ptr)
        return ret


    def GetText(self ,rowIndex:int,columnIndex:int)->str:
        """
    <summary>
        Get value from the current table
    </summary>
    <param name="rowIndex">the row index,the index starts at 0</param>
    <param name="columnIndex">the column index,the index starts at 0</param>
    <returns>the text</returns>
        """
        
        GetDllLibPdf().Utilities_PdfTable_GetText.argtypes=[c_void_p ,c_int,c_int]
        GetDllLibPdf().Utilities_PdfTable_GetText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Utilities_PdfTable_GetText(self.Ptr, rowIndex,columnIndex))
        return ret


