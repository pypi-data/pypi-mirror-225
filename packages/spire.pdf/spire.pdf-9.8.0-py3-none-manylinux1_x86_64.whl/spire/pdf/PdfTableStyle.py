from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTableStyle (SpireObject) :
    """
    <summary>
        Represents parameters of PdfTable.
    </summary>
    """
    @property
    def IsFixWidth(self)->bool:
        """
    <summary>
        get or set the value of fitWidth.
    </summary>
        """
        GetDllLibPdf().PdfTableStyle_get_IsFixWidth.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_IsFixWidth.restype=c_bool
        ret = GetDllLibPdf().PdfTableStyle_get_IsFixWidth(self.Ptr)
        return ret

    @IsFixWidth.setter
    def IsFixWidth(self, value:bool):
        GetDllLibPdf().PdfTableStyle_set_IsFixWidth.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTableStyle_set_IsFixWidth(self.Ptr, value)

    @property

    def DefaultStyle(self)->'PdfCellStyle':
        """
    <summary>
        Gets or sets the default cell style.
    </summary>
        """
        GetDllLibPdf().PdfTableStyle_get_DefaultStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_DefaultStyle.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTableStyle_get_DefaultStyle(self.Ptr)
        ret = None if intPtr==None else PdfCellStyle(intPtr)
        return ret


    @DefaultStyle.setter
    def DefaultStyle(self, value:'PdfCellStyle'):
        GetDllLibPdf().PdfTableStyle_set_DefaultStyle.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfTableStyle_set_DefaultStyle(self.Ptr, value.Ptr)

    @property

    def AlternateStyle(self)->'PdfCellStyle':
        """
    <summary>
        Gets or sets the odd row cell style.
    </summary>
        """
        GetDllLibPdf().PdfTableStyle_get_AlternateStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_AlternateStyle.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTableStyle_get_AlternateStyle(self.Ptr)
        ret = None if intPtr==None else PdfCellStyle(intPtr)
        return ret


    @AlternateStyle.setter
    def AlternateStyle(self, value:'PdfCellStyle'):
        GetDllLibPdf().PdfTableStyle_set_AlternateStyle.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfTableStyle_set_AlternateStyle(self.Ptr, value.Ptr)

    @property

    def HeaderSource(self)->'PdfHeaderSource':
        """
    <summary>
        Gets or sets a value indicating whether
            to use rows or column captions for forming header.
    </summary>
        """
        GetDllLibPdf().PdfTableStyle_get_HeaderSource.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_HeaderSource.restype=c_int
        ret = GetDllLibPdf().PdfTableStyle_get_HeaderSource(self.Ptr)
        objwraped = PdfHeaderSource(ret)
        return objwraped

    @HeaderSource.setter
    def HeaderSource(self, value:'PdfHeaderSource'):
        GetDllLibPdf().PdfTableStyle_set_HeaderSource.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfTableStyle_set_HeaderSource(self.Ptr, value.value)

    @property
    def HeaderRowCount(self)->int:
        """
    <summary>
        Gets or sets the header rows count.
    </summary>
        """
        GetDllLibPdf().PdfTableStyle_get_HeaderRowCount.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_HeaderRowCount.restype=c_int
        ret = GetDllLibPdf().PdfTableStyle_get_HeaderRowCount(self.Ptr)
        return ret

    @HeaderRowCount.setter
    def HeaderRowCount(self, value:int):
        GetDllLibPdf().PdfTableStyle_set_HeaderRowCount.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfTableStyle_set_HeaderRowCount(self.Ptr, value)

    @property

    def HeaderStyle(self)->'PdfCellStyle':
        """
    <summary>
        Gets or sets the header cell style.
    </summary>
        """
        GetDllLibPdf().PdfTableStyle_get_HeaderStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_HeaderStyle.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTableStyle_get_HeaderStyle(self.Ptr)
        ret = None if intPtr==None else PdfCellStyle(intPtr)
        return ret


    @HeaderStyle.setter
    def HeaderStyle(self, value:'PdfCellStyle'):
        GetDllLibPdf().PdfTableStyle_set_HeaderStyle.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfTableStyle_set_HeaderStyle(self.Ptr, value.Ptr)

    @property
    def RepeatHeader(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to repeat header on each page.
    </summary>
        """
        GetDllLibPdf().PdfTableStyle_get_RepeatHeader.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_RepeatHeader.restype=c_bool
        ret = GetDllLibPdf().PdfTableStyle_get_RepeatHeader(self.Ptr)
        return ret

    @RepeatHeader.setter
    def RepeatHeader(self, value:bool):
        GetDllLibPdf().PdfTableStyle_set_RepeatHeader.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTableStyle_set_RepeatHeader(self.Ptr, value)

    @property
    def ShowHeader(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether the header is visible.
    </summary>
<remarks>If the header is made up with ordinary rows they aren't visible
            while this property is set to false.</remarks>
        """
        GetDllLibPdf().PdfTableStyle_get_ShowHeader.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_ShowHeader.restype=c_bool
        ret = GetDllLibPdf().PdfTableStyle_get_ShowHeader(self.Ptr)
        return ret

    @ShowHeader.setter
    def ShowHeader(self, value:bool):
        GetDllLibPdf().PdfTableStyle_set_ShowHeader.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTableStyle_set_ShowHeader(self.Ptr, value)

    @property
    def CellSpacing(self)->float:
        """
    <summary>
        Gets or sets the cell spacing.
    </summary>
        """
        GetDllLibPdf().PdfTableStyle_get_CellSpacing.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_CellSpacing.restype=c_float
        ret = GetDllLibPdf().PdfTableStyle_get_CellSpacing(self.Ptr)
        return ret

    @CellSpacing.setter
    def CellSpacing(self, value:float):
        GetDllLibPdf().PdfTableStyle_set_CellSpacing.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfTableStyle_set_CellSpacing(self.Ptr, value)

    @property
    def CellPadding(self)->float:
        """
    <summary>
        Gets or sets the cell padding.
    </summary>
        """
        GetDllLibPdf().PdfTableStyle_get_CellPadding.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_CellPadding.restype=c_float
        ret = GetDllLibPdf().PdfTableStyle_get_CellPadding(self.Ptr)
        return ret

    @CellPadding.setter
    def CellPadding(self, value:float):
        GetDllLibPdf().PdfTableStyle_set_CellPadding.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfTableStyle_set_CellPadding(self.Ptr, value)

    @property

    def BorderOverlapStyle(self)->'PdfBorderOverlapStyle':
        """
    <summary>
        Gets or sets a value indicating whether the cell borders
            should overlap its neighbour's borders or be drawn in the cell interior.
    </summary>
<remarks>Please, use this property with caution,
            because it might cause unexpected results if borders
            are not the same width and colour.</remarks>
        """
        GetDllLibPdf().PdfTableStyle_get_BorderOverlapStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_BorderOverlapStyle.restype=c_int
        ret = GetDllLibPdf().PdfTableStyle_get_BorderOverlapStyle(self.Ptr)
        objwraped = PdfBorderOverlapStyle(ret)
        return objwraped

    @BorderOverlapStyle.setter
    def BorderOverlapStyle(self, value:'PdfBorderOverlapStyle'):
        GetDllLibPdf().PdfTableStyle_set_BorderOverlapStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfTableStyle_set_BorderOverlapStyle(self.Ptr, value.value)

    @property

    def BorderPen(self)->'PdfPen':
        """
    <summary>
        Gets or sets the pen of the table border.
    </summary>
        """
        GetDllLibPdf().PdfTableStyle_get_BorderPen.argtypes=[c_void_p]
        GetDllLibPdf().PdfTableStyle_get_BorderPen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTableStyle_get_BorderPen(self.Ptr)
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @BorderPen.setter
    def BorderPen(self, value:'PdfPen'):
        GetDllLibPdf().PdfTableStyle_set_BorderPen.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfTableStyle_set_BorderPen(self.Ptr, value.Ptr)

