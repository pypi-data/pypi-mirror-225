from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfUsedFont (SpireObject) :
    """
    <summary>
        Represents the used fonts in a PDF document.
    </summary>
    """
    @property

    def Name(self)->str:
        """
    <summary>
        Gets the name.
    </summary>
<value>The name.</value>
        """
        GetDllLibPdf().PdfUsedFont_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().PdfUsedFont_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfUsedFont_get_Name(self.Ptr))
        return ret


    @property
    def Size(self)->float:
        """
    <summary>
        Gets the size.
    </summary>
<value>The size.</value>
        """
        GetDllLibPdf().PdfUsedFont_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfUsedFont_get_Size.restype=c_float
        ret = GetDllLibPdf().PdfUsedFont_get_Size(self.Ptr)
        return ret

    @property

    def Style(self)->'PdfFontStyle':
        """
    <summary>
        Gets the style.
    </summary>
<value>The style.</value>
        """
        GetDllLibPdf().PdfUsedFont_get_Style.argtypes=[c_void_p]
        GetDllLibPdf().PdfUsedFont_get_Style.restype=c_int
        ret = GetDllLibPdf().PdfUsedFont_get_Style(self.Ptr)
        objwraped = PdfFontStyle(ret)
        return objwraped

    @property

    def Type(self)->'PdfFontType':
        """
    <summary>
        Gets the type.
    </summary>
<value>The type.</value>
        """
        GetDllLibPdf().PdfUsedFont_get_Type.argtypes=[c_void_p]
        GetDllLibPdf().PdfUsedFont_get_Type.restype=c_int
        ret = GetDllLibPdf().PdfUsedFont_get_Type(self.Ptr)
        objwraped = PdfFontType(ret)
        return objwraped


    def Replace(self ,fontToReplace:'PdfFontBase'):
        """
    <summary>
        Replaces the specified new font.
    </summary>
    <param name="newFont">The new font.</param>
        """
        intPtrfontToReplace:c_void_p = fontToReplace.Ptr

        GetDllLibPdf().PdfUsedFont_Replace.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfUsedFont_Replace(self.Ptr, intPtrfontToReplace)

    @staticmethod

    def ScaleFontSize(page:'PdfPageBase',fontNames:List[str],factor:float):
        """
    <summary>
        Scale the font size specified page.
    </summary>
    <param name="page">modified page</param>
    <param name="fontNames">the names of the fonts to be scaled</param>
    <param name="factor">scale factor</param>
        """
        intPtrpage:c_void_p = page.Ptr
        #arrayfontNames:ArrayTypefontNames = ""
        countfontNames = len(fontNames)
        ArrayTypefontNames = c_wchar_p * countfontNames
        arrayfontNames = ArrayTypefontNames()
        for i in range(0, countfontNames):
            arrayfontNames[i] = fontNames[i]


        GetDllLibPdf().PdfUsedFont_ScaleFontSize.argtypes=[ c_void_p,c_void_p,ArrayTypefontNames,c_int,c_float]
        GetDllLibPdf().PdfUsedFont_ScaleFontSize(None, intPtrpage,arrayfontNames,countfontNames,factor)

    def Dispose(self):
        """
    <summary>
        Dispose font
    </summary>
        """
        GetDllLibPdf().PdfUsedFont_Dispose.argtypes=[c_void_p]
        GetDllLibPdf().PdfUsedFont_Dispose(self.Ptr)

