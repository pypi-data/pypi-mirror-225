from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridCellStyle (  PdfGridRowStyle) :
    """
    <summary>
        Grid cell style
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
        GetDllLibPdf().PdfGridCellStyle_get_CellPadding.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellStyle_get_CellPadding.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCellStyle_get_CellPadding(self.Ptr)
        ret = None if intPtr==None else PdfPaddings(intPtr)
        return ret


    @CellPadding.setter
    def CellPadding(self, value:'PdfPaddings'):
        GetDllLibPdf().PdfGridCellStyle_set_CellPadding.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCellStyle_set_CellPadding(self.Ptr, value.Ptr)

    @property

    def StringFormat(self)->'PdfStringFormat':
        """
    <summary>
        Gets the string format.
    </summary>
<value>The string format.</value>
        """
        GetDllLibPdf().PdfGridCellStyle_get_StringFormat.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellStyle_get_StringFormat.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCellStyle_get_StringFormat(self.Ptr)
        ret = None if intPtr==None else PdfStringFormat(intPtr)
        return ret


    @StringFormat.setter
    def StringFormat(self, value:'PdfStringFormat'):
        GetDllLibPdf().PdfGridCellStyle_set_StringFormat.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCellStyle_set_StringFormat(self.Ptr, value.Ptr)

    @property

    def Borders(self)->'PdfBorders':
        """
    <summary>
        Gets or sets the border.
    </summary>
<value>The border.</value>
        """
        GetDllLibPdf().PdfGridCellStyle_get_Borders.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellStyle_get_Borders.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCellStyle_get_Borders(self.Ptr)
        ret = None if intPtr==None else PdfBorders(intPtr)
        return ret


    @Borders.setter
    def Borders(self, value:'PdfBorders'):
        GetDllLibPdf().PdfGridCellStyle_set_Borders.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCellStyle_set_Borders(self.Ptr, value.Ptr)

    @property

    def BackgroundImage(self)->'PdfImage':
        """
    <summary>
        Gets or sets the background image.
    </summary>
<value>The background image.</value>
        """
        GetDllLibPdf().PdfGridCellStyle_get_BackgroundImage.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellStyle_get_BackgroundImage.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCellStyle_get_BackgroundImage(self.Ptr)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @BackgroundImage.setter
    def BackgroundImage(self, value:'PdfImage'):
        GetDllLibPdf().PdfGridCellStyle_set_BackgroundImage.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCellStyle_set_BackgroundImage(self.Ptr, value.Ptr)

