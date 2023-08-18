from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class LineBorder (SpireObject) :
    """
    <summary>
        Represents the border style of the Line annotation.
    </summary>
    """
    @property
    def BorderWidth(self)->int:
        """
    <summary>
        Gets or sets the width.
    </summary>
<value>The line border width.</value>
        """
        GetDllLibPdf().LineBorder_get_BorderWidth.argtypes=[c_void_p]
        GetDllLibPdf().LineBorder_get_BorderWidth.restype=c_int
        ret = GetDllLibPdf().LineBorder_get_BorderWidth(self.Ptr)
        return ret

    @BorderWidth.setter
    def BorderWidth(self, value:int):
        GetDllLibPdf().LineBorder_set_BorderWidth.argtypes=[c_void_p, c_int]
        GetDllLibPdf().LineBorder_set_BorderWidth(self.Ptr, value)

    @property

    def BorderStyle(self)->'PdfBorderStyle':
        """
    <summary>
        Gets or sets the border style.
    </summary>
<value>The line border style.</value>
        """
        GetDllLibPdf().LineBorder_get_BorderStyle.argtypes=[c_void_p]
        GetDllLibPdf().LineBorder_get_BorderStyle.restype=c_int
        ret = GetDllLibPdf().LineBorder_get_BorderStyle(self.Ptr)
        objwraped = PdfBorderStyle(ret)
        return objwraped

    @BorderStyle.setter
    def BorderStyle(self, value:'PdfBorderStyle'):
        GetDllLibPdf().LineBorder_set_BorderStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().LineBorder_set_BorderStyle(self.Ptr, value.value)

    @property
    def DashArray(self)->int:
        """
    <summary>
        Gets or sets the Line Dash
    </summary>
<value>The line border dash array.</value>
        """
        GetDllLibPdf().LineBorder_get_DashArray.argtypes=[c_void_p]
        GetDllLibPdf().LineBorder_get_DashArray.restype=c_int
        ret = GetDllLibPdf().LineBorder_get_DashArray(self.Ptr)
        return ret

    @DashArray.setter
    def DashArray(self, value:int):
        GetDllLibPdf().LineBorder_set_DashArray.argtypes=[c_void_p, c_int]
        GetDllLibPdf().LineBorder_set_DashArray(self.Ptr, value)

