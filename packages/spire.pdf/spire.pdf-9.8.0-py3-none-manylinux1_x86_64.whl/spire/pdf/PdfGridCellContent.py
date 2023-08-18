from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridCellContent (SpireObject) :
    """
    <summary>
        Represents the content that can be written in a grid cell.
    </summary>
    """
    @property
    def ImageLocation(self)->'PointF':
        return None

    @ImageLocation.setter
    def ImageLocation(self, value:'PointF'):
        GetDllLibPdf().PdfGridCellContent_set_ImageLocation.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCellContent_set_ImageLocation(self.Ptr, value.Ptr)

    @property

    def Text(self)->str:
        """

        """
        GetDllLibPdf().PdfGridCellContent_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellContent_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfGridCellContent_get_Text(self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        GetDllLibPdf().PdfGridCellContent_set_Text.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfGridCellContent_set_Text(self.Ptr, value)

    @property

    def Brush(self)->'PdfBrush':
        """

        """
        GetDllLibPdf().PdfGridCellContent_get_Brush.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellContent_get_Brush.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCellContent_get_Brush(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @Brush.setter
    def Brush(self, value:'PdfBrush'):
        GetDllLibPdf().PdfGridCellContent_set_Brush.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCellContent_set_Brush(self.Ptr, value.Ptr)

    @property

    def Font(self)->'PdfFontBase':
        """

        """
        GetDllLibPdf().PdfGridCellContent_get_Font.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellContent_get_Font.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCellContent_get_Font(self.Ptr)
        ret = None if intPtr==None else PdfFontBase(intPtr)
        return ret


    @Font.setter
    def Font(self, value:'PdfFontBase'):
        GetDllLibPdf().PdfGridCellContent_set_Font.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCellContent_set_Font(self.Ptr, value.Ptr)

    @property

    def Image(self)->'PdfImage':
        """

        """
        GetDllLibPdf().PdfGridCellContent_get_Image.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellContent_get_Image.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCellContent_get_Image(self.Ptr)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @Image.setter
    def Image(self, value:'PdfImage'):
        GetDllLibPdf().PdfGridCellContent_set_Image.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCellContent_set_Image(self.Ptr, value.Ptr)

    @property

    def ImageSize(self)->'SizeF':
        """

        """
        GetDllLibPdf().PdfGridCellContent_get_ImageSize.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellContent_get_ImageSize.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCellContent_get_ImageSize(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @ImageSize.setter
    def ImageSize(self, value:'SizeF'):
        GetDllLibPdf().PdfGridCellContent_set_ImageSize.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCellContent_set_ImageSize(self.Ptr, value.Ptr)

    @property
    def ImageNewline(self)->bool:
        """

        """
        GetDllLibPdf().PdfGridCellContent_get_ImageNewline.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellContent_get_ImageNewline.restype=c_bool
        ret = GetDllLibPdf().PdfGridCellContent_get_ImageNewline(self.Ptr)
        return ret

    @ImageNewline.setter
    def ImageNewline(self, value:bool):
        GetDllLibPdf().PdfGridCellContent_set_ImageNewline.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfGridCellContent_set_ImageNewline(self.Ptr, value)

    @property

    def StringFormat(self)->'PdfStringFormat':
        """

        """
        GetDllLibPdf().PdfGridCellContent_get_StringFormat.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridCellContent_get_StringFormat.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridCellContent_get_StringFormat(self.Ptr)
        ret = None if intPtr==None else PdfStringFormat(intPtr)
        return ret


    @StringFormat.setter
    def StringFormat(self, value:'PdfStringFormat'):
        GetDllLibPdf().PdfGridCellContent_set_StringFormat.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridCellContent_set_StringFormat(self.Ptr, value.Ptr)

