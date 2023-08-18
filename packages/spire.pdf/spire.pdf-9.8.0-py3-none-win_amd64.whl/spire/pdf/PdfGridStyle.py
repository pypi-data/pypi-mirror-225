from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridStyle (  PdfGridStyleBase) :
    """
    <summary>
        Grid style
    </summary>
    """
    @property
    def CellSpacing(self)->float:
        """
    <summary>
        Gets or sets the cell spacing.
    </summary>
<value>The cell spacing.</value>
        """
        GetDllLibPdf().PdfGridStyle_get_CellSpacing.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridStyle_get_CellSpacing.restype=c_float
        ret = GetDllLibPdf().PdfGridStyle_get_CellSpacing(self.Ptr)
        return ret

    @CellSpacing.setter
    def CellSpacing(self, value:float):
        GetDllLibPdf().PdfGridStyle_set_CellSpacing.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfGridStyle_set_CellSpacing(self.Ptr, value)

    @property

    def CellPadding(self)->'PdfPaddings':
        """
    <summary>
        Gets or sets the cell padding.
    </summary>
<value>The cell padding.</value>
        """
        GetDllLibPdf().PdfGridStyle_get_CellPadding.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridStyle_get_CellPadding.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridStyle_get_CellPadding(self.Ptr)
        ret = None if intPtr==None else PdfPaddings(intPtr)
        return ret


    @CellPadding.setter
    def CellPadding(self, value:'PdfPaddings'):
        GetDllLibPdf().PdfGridStyle_set_CellPadding.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridStyle_set_CellPadding(self.Ptr, value.Ptr)

    @property

    def BorderOverlapStyle(self)->'PdfBorderOverlapStyle':
        """
    <summary>
        Gets or sets the border overlap style.
    </summary>
<value>The border overlap style.</value>
        """
        GetDllLibPdf().PdfGridStyle_get_BorderOverlapStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridStyle_get_BorderOverlapStyle.restype=c_int
        ret = GetDllLibPdf().PdfGridStyle_get_BorderOverlapStyle(self.Ptr)
        objwraped = PdfBorderOverlapStyle(ret)
        return objwraped

    @BorderOverlapStyle.setter
    def BorderOverlapStyle(self, value:'PdfBorderOverlapStyle'):
        GetDllLibPdf().PdfGridStyle_set_BorderOverlapStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfGridStyle_set_BorderOverlapStyle(self.Ptr, value.value)

    @property
    def AllowHorizontalOverflow(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to allow horizontal overflow.
    </summary>
<value>
  <c>true</c> if [allow horizontal overflow]; otherwise, <c>false</c>.
            </value>
        """
        GetDllLibPdf().PdfGridStyle_get_AllowHorizontalOverflow.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridStyle_get_AllowHorizontalOverflow.restype=c_bool
        ret = GetDllLibPdf().PdfGridStyle_get_AllowHorizontalOverflow(self.Ptr)
        return ret

    @AllowHorizontalOverflow.setter
    def AllowHorizontalOverflow(self, value:bool):
        GetDllLibPdf().PdfGridStyle_set_AllowHorizontalOverflow.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfGridStyle_set_AllowHorizontalOverflow(self.Ptr, value)

    @property

    def HorizontalOverflowType(self)->'PdfHorizontalOverflowType':
        """
    <summary>
        Gets or sets the type of the horizontal overflow.
    </summary>
<value>The type of the horizontal overflow.</value>
        """
        GetDllLibPdf().PdfGridStyle_get_HorizontalOverflowType.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridStyle_get_HorizontalOverflowType.restype=c_int
        ret = GetDllLibPdf().PdfGridStyle_get_HorizontalOverflowType(self.Ptr)
        objwraped = PdfHorizontalOverflowType(ret)
        return objwraped

    @HorizontalOverflowType.setter
    def HorizontalOverflowType(self, value:'PdfHorizontalOverflowType'):
        GetDllLibPdf().PdfGridStyle_set_HorizontalOverflowType.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfGridStyle_set_HorizontalOverflowType(self.Ptr, value.value)

