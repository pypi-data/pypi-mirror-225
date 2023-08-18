from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridColumn (SpireObject) :
    """

    """
    @property
    def Width(self)->float:
        """
    <summary>
        Gets or sets the width. The with is equal to the content 
            width plus margin plus half of the left and right borders.
    </summary>
<value>The width.</value>
        """
        GetDllLibPdf().PdfGridColumn_get_Width.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridColumn_get_Width.restype=c_float
        ret = GetDllLibPdf().PdfGridColumn_get_Width(self.Ptr)
        return ret

    @Width.setter
    def Width(self, value:float):
        GetDllLibPdf().PdfGridColumn_set_Width.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfGridColumn_set_Width(self.Ptr, value)

    @property

    def Format(self)->'PdfStringFormat':
        """
    <summary>
        Gets or sets the format.
    </summary>
<value>The format.</value>
        """
        GetDllLibPdf().PdfGridColumn_get_Format.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridColumn_get_Format.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridColumn_get_Format(self.Ptr)
        ret = None if intPtr==None else PdfStringFormat(intPtr)
        return ret


    @Format.setter
    def Format(self, value:'PdfStringFormat'):
        GetDllLibPdf().PdfGridColumn_set_Format.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridColumn_set_Format(self.Ptr, value.Ptr)

    @property

    def Grid(self)->'PdfGrid':
        """
    <summary>
        Gets the grid.
    </summary>
<value>The grid.</value>
        """
        GetDllLibPdf().PdfGridColumn_get_Grid.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridColumn_get_Grid.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridColumn_get_Grid(self.Ptr)
        ret = None if intPtr==None else PdfGrid(intPtr)
        return ret


