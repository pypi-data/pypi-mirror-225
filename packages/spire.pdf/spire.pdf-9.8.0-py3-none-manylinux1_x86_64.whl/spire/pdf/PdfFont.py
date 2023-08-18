from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFont (  PdfFontBase) :

    @dispatch
    def __init__(self, fontFamily:PdfFontFamily,size:float):
        enumfontFamily:c_int = fontFamily.value
        GetDllLibPdf().PdfFont_CreatePdfFontFS.argtypes=[c_int,c_float]
        GetDllLibPdf().PdfFont_CreatePdfFontFS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfFont_CreatePdfFontFS(enumfontFamily,size)
        super(PdfFont, self).__init__(intPtr)

    @dispatch
    def __init__(self, fontFamily:PdfFontFamily,size:float,style:PdfFontStyle):
        enumfontFamily:c_int = fontFamily.value
        enumstyle:c_int = style.value
        GetDllLibPdf().PdfFont_CreatePdfFontFSS.argtypes=[c_int,c_float,c_int]
        GetDllLibPdf().PdfFont_CreatePdfFontFSS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfFont_CreatePdfFontFSS(enumfontFamily,size,enumstyle)
        super(PdfFont, self).__init__(intPtr)

    """
    <summary>
        Represents one of the 14 standard PDF fonts.
    </summary>
    """
    @property

    def FontFamily(self)->'PdfFontFamily':
        """
    <summary>
        Gets the FontFamily.
    </summary>
        """
        GetDllLibPdf().PdfFont_get_FontFamily.argtypes=[c_void_p]
        GetDllLibPdf().PdfFont_get_FontFamily.restype=c_int
        ret = GetDllLibPdf().PdfFont_get_FontFamily(self.Ptr)
        objwraped = PdfFontFamily(ret)
        return objwraped

