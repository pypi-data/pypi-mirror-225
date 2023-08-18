from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridRowStyle (  PdfGridStyleBase) :
    """
    <summary>
        Grid row style
    </summary>
    """
    @property

    def CellPadding(self)->'PdfPaddings':
        """
    <summary>
        Get or sets the cell padding.
    </summary>
    <returns>The cell padding.</returns>
        """
        GetDllLibPdf().PdfGridRowStyle_get_CellPadding.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridRowStyle_get_CellPadding.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridRowStyle_get_CellPadding(self.Ptr)
        ret = None if intPtr==None else PdfPaddings(intPtr)
        return ret


    @CellPadding.setter
    def CellPadding(self, value:'PdfPaddings'):
        GetDllLibPdf().PdfGridRowStyle_set_CellPadding.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridRowStyle_set_CellPadding(self.Ptr, value.Ptr)

