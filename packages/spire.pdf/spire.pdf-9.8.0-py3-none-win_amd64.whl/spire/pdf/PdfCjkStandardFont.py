from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc


class PdfCjkStandardFont (  PdfFontBase) :
    @dispatch
    def __init__(self, fontFamily:PdfCjkFontFamily , size:float , style:PdfFontStyle ):
        enumCjkFont:c_int = fontFamily.value
        enumFontStyle:c_int = style.value
        GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontFSS.argtypes=[c_int,c_float,c_int]
        GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontFSS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontFSS(enumCjkFont,size,enumFontStyle)
        super(PdfCjkStandardFont, self).__init__(intPtr)

    @dispatch
    def __init__(self, fontFamily:PdfCjkFontFamily , size:float ):
        enumCjkFont:c_int = fontFamily.value
        GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontFS.argtypes=[c_int,c_float]
        GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontFS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontFS(enumCjkFont,size)
        super(PdfCjkStandardFont, self).__init__(intPtr)
    
    @dispatch
    def __init__(self, prototype , size:float ):
        ptrType:c_void_p = prototype.Ptr
        GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontPS.argtypes=[c_void_p,c_float]
        GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontPS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontPS(ptrType,size)
        super(PdfCjkStandardFont, self).__init__(intPtr)

    @dispatch
    def __init__(self, prototype , size:float, style:PdfFontStyle ):
        ptrType:c_void_p = prototype.Ptr
        enumFontStyle:c_int = style.value
        GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontPSS.argtypes=[c_void_p,c_float,c_int]
        GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontPSS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCjkStandardFont_CreatePdfCjkStandardFontPSS(ptrType,size,enumFontStyle)
        super(PdfCjkStandardFont, self).__init__(intPtr)
    """
    <summary>
        Represents the standard CJK fonts.
    </summary>
    """
    @property

    def FontFamily(self)->'PdfCjkFontFamily':
        """
    <summary>
        Gets the font family.
    </summary>
        """
        GetDllLibPdf().PdfCjkStandardFont_get_FontFamily.argtypes=[c_void_p]
        GetDllLibPdf().PdfCjkStandardFont_get_FontFamily.restype=c_int
        ret = GetDllLibPdf().PdfCjkStandardFont_get_FontFamily(self.Ptr)
        objwraped = PdfCjkFontFamily(ret)
        return objwraped

