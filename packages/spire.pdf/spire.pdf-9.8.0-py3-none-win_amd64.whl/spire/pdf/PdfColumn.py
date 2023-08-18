from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfColumn (SpireObject) :
    """
    <summary>
        Represents a single column of the table.
    </summary>
    """
    @property

    def StringFormat(self)->'PdfStringFormat':
        """
    <summary>
        Gets or sets the string format.
    </summary>
<value>The string format.</value>
        """
        GetDllLibPdf().PdfColumn_get_StringFormat.argtypes=[c_void_p]
        GetDllLibPdf().PdfColumn_get_StringFormat.restype=c_void_p
        intPtr = GetDllLibPdf().PdfColumn_get_StringFormat(self.Ptr)
        ret = None if intPtr==None else PdfStringFormat(intPtr)
        return ret


    @StringFormat.setter
    def StringFormat(self, value:'PdfStringFormat'):
        GetDllLibPdf().PdfColumn_set_StringFormat.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfColumn_set_StringFormat(self.Ptr, value.Ptr)

    @property
    def Width(self)->float:
        """
    <summary>
        Gets or sets the width of the column.
    </summary>
        """
        GetDllLibPdf().PdfColumn_get_Width.argtypes=[c_void_p]
        GetDllLibPdf().PdfColumn_get_Width.restype=c_float
        ret = GetDllLibPdf().PdfColumn_get_Width(self.Ptr)
        return ret

    @Width.setter
    def Width(self, value:float):
        GetDllLibPdf().PdfColumn_set_Width.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfColumn_set_Width(self.Ptr, value)

    @property

    def ColumnName(self)->str:
        """
    <summary>
        Gets or sets the column name.
    </summary>
        """
        GetDllLibPdf().PdfColumn_get_ColumnName.argtypes=[c_void_p]
        GetDllLibPdf().PdfColumn_get_ColumnName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfColumn_get_ColumnName(self.Ptr))
        return ret


    @ColumnName.setter
    def ColumnName(self, value:str):
        GetDllLibPdf().PdfColumn_set_ColumnName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfColumn_set_ColumnName(self.Ptr, value)

