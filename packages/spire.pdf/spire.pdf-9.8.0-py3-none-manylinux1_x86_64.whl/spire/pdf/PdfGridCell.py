from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridCell (SpireObject) :
    """

    """
    @property
    def Width(self)->float:
        """
    <summary>
        Gets or sets the width.
    </summary>
<value>The width.</value>
        """
        GetDllLibPdf().PdfGridCell_get_Width.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCell_get_Width.restype=c_float
        ret = GetDllLibPdf().PdfGridCell_get_Width(self.Ptr)
        return ret

    @property
    def Height(self)->float:
        """
    <summary>
        Gets the height.
    </summary>
<value>The height.</value>
        """
        GetDllLibPdf().PdfGridCell_get_Height.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCell_get_Height.restype=c_float
        ret = GetDllLibPdf().PdfGridCell_get_Height(self.Ptr)
        return ret

    @property
    def RowSpan(self)->int:
        """
    <summary>
        Gets or sets the row span.
    </summary>
<value>The row span.</value>
        """
        GetDllLibPdf().PdfGridCell_get_RowSpan.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCell_get_RowSpan.restype=c_int
        ret = GetDllLibPdf().PdfGridCell_get_RowSpan(self.Ptr)
        return ret

    @RowSpan.setter
    def RowSpan(self, value:int):
        GetDllLibPdf().PdfGridCell_set_RowSpan.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfGridCell_set_RowSpan(self.Ptr, value)

    @property
    def ColumnSpan(self)->int:
        """
    <summary>
        Gets or sets the column span.
    </summary>
<value>The column span.</value>
        """
        GetDllLibPdf().PdfGridCell_get_ColumnSpan.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCell_get_ColumnSpan.restype=c_int
        ret = GetDllLibPdf().PdfGridCell_get_ColumnSpan(self.Ptr)
        return ret

    @ColumnSpan.setter
    def ColumnSpan(self, value:int):
        GetDllLibPdf().PdfGridCell_set_ColumnSpan.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfGridCell_set_ColumnSpan(self.Ptr, value)

    @property

    def Style(self)->'PdfGridCellStyle':
        """
    <summary>
        Gets or sets the cell style.
    </summary>
<value>The cell style.</value>
        """
        GetDllLibPdf().PdfGridCell_get_Style.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCell_get_Style.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCell_get_Style(self.Ptr)
        ret = None if intPtr==None else PdfGridCellStyle(intPtr)
        return ret


    @Style.setter
    def Style(self, value:'PdfGridCellStyle'):
        GetDllLibPdf().PdfGridCell_set_Style.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCell_set_Style(self.Ptr, value.Ptr)

    @property

    def Value(self)->'SpireObject':
        """
    <summary>
        Gets or sets the value.
    </summary>
<value>The value.</value>
        """
        GetDllLibPdf().PdfGridCell_get_Value.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCell_get_Value.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCell_get_Value(self.Ptr)
        ret = None if intPtr==None else SpireObject(intPtr)
        return ret


    @Value.setter
    def Value(self, value:'SpireObject'):
        GetDllLibPdf().PdfGridCell_set_Value.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCell_set_Value(self.Ptr, value.Ptr)

    @property

    def StringFormat(self)->'PdfStringFormat':
        """
    <summary>
        Gets or sets the string format.
    </summary>
<value>The string format.</value>
        """
        GetDllLibPdf().PdfGridCell_get_StringFormat.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCell_get_StringFormat.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCell_get_StringFormat(self.Ptr)
        ret = None if intPtr==None else PdfStringFormat(intPtr)
        return ret


    @StringFormat.setter
    def StringFormat(self, value:'PdfStringFormat'):
        GetDllLibPdf().PdfGridCell_set_StringFormat.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCell_set_StringFormat(self.Ptr, value.Ptr)

