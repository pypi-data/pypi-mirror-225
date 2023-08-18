from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridStyleBase (SpireObject) :
    """
<summary></summary>
    """
    @property

    def BackgroundBrush(self)->'PdfBrush':
        """
    <summary>
        Gets or sets the background brush.
    </summary>
<value>The background brush.</value>
        """
        GetDllLibPdf().PdfGridStyleBase_get_BackgroundBrush.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridStyleBase_get_BackgroundBrush.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridStyleBase_get_BackgroundBrush(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @BackgroundBrush.setter
    def BackgroundBrush(self, value:'PdfBrush'):
        GetDllLibPdf().PdfGridStyleBase_set_BackgroundBrush.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridStyleBase_set_BackgroundBrush(self.Ptr, value.Ptr)

    @property

    def TextBrush(self)->'PdfBrush':
        """
    <summary>
        Gets or sets the text brush.
    </summary>
<value>The text brush.</value>
        """
        GetDllLibPdf().PdfGridStyleBase_get_TextBrush.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridStyleBase_get_TextBrush.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridStyleBase_get_TextBrush(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @TextBrush.setter
    def TextBrush(self, value:'PdfBrush'):
        GetDllLibPdf().PdfGridStyleBase_set_TextBrush.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridStyleBase_set_TextBrush(self.Ptr, value.Ptr)

    @property

    def TextPen(self)->'PdfPen':
        """
    <summary>
        Gets or sets the text pen.
    </summary>
<value>The text pen.</value>
        """
        GetDllLibPdf().PdfGridStyleBase_get_TextPen.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridStyleBase_get_TextPen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridStyleBase_get_TextPen(self.Ptr)
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @TextPen.setter
    def TextPen(self, value:'PdfPen'):
        GetDllLibPdf().PdfGridStyleBase_set_TextPen.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridStyleBase_set_TextPen(self.Ptr, value.Ptr)

    @property

    def Font(self)->'PdfFontBase':
        """
    <summary>
        Gets or sets the font.
    </summary>
<value>The font.</value>
        """
        GetDllLibPdf().PdfGridStyleBase_get_Font.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridStyleBase_get_Font.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridStyleBase_get_Font(self.Ptr)
        ret = None if intPtr==None else PdfFontBase(intPtr)
        return ret


    @Font.setter
    def Font(self, value:'PdfFontBase'):
        GetDllLibPdf().PdfGridStyleBase_set_Font.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGridStyleBase_set_Font(self.Ptr, value.Ptr)


    def Clone(self)->'SpireObject':
        """
    <summary>
        Creates a new object that is a copy of the current instance.
    </summary>
    <returns>
            A new object that is a copy of this instance.
            </returns>
        """
        GetDllLibPdf().PdfGridStyleBase_Clone.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridStyleBase_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGridStyleBase_Clone(self.Ptr)
        ret = None if intPtr==None else SpireObject(intPtr)
        return ret


