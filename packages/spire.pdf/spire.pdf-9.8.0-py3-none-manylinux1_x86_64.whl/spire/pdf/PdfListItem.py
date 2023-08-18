from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfListItem (SpireObject) :
    """
    <summary>
        Represents the list item of the list.
    </summary>
    """
    @property

    def Font(self)->'PdfFontBase':
        """
    <summary>
        Gets or sets item font.
    </summary>
        """
        GetDllLibPdf().PdfListItem_get_Font.argtypes=[c_void_p]
        GetDllLibPdf().PdfListItem_get_Font.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListItem_get_Font(self.Ptr)
        ret = None if intPtr==None else PdfFontBase(intPtr)
        return ret


    @Font.setter
    def Font(self, value:'PdfFontBase'):
        GetDllLibPdf().PdfListItem_set_Font.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfListItem_set_Font(self.Ptr, value.Ptr)

    @property

    def Text(self)->str:
        """
    <summary>
        Gets or sets item text.
    </summary>
        """
        GetDllLibPdf().PdfListItem_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfListItem_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfListItem_get_Text(self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        GetDllLibPdf().PdfListItem_set_Text.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfListItem_set_Text(self.Ptr, value)

    @property

    def StringFormat(self)->'PdfStringFormat':
        """
    <summary>
        Gets or sets item string format.
    </summary>
        """
        GetDllLibPdf().PdfListItem_get_StringFormat.argtypes=[c_void_p]
        GetDllLibPdf().PdfListItem_get_StringFormat.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListItem_get_StringFormat(self.Ptr)
        ret = None if intPtr==None else PdfStringFormat(intPtr)
        return ret


    @StringFormat.setter
    def StringFormat(self, value:'PdfStringFormat'):
        GetDllLibPdf().PdfListItem_set_StringFormat.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfListItem_set_StringFormat(self.Ptr, value.Ptr)

    @property

    def Pen(self)->'PdfPen':
        """
    <summary>
        Gets or sets list item pen.
    </summary>
        """
        GetDllLibPdf().PdfListItem_get_Pen.argtypes=[c_void_p]
        GetDllLibPdf().PdfListItem_get_Pen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListItem_get_Pen(self.Ptr)
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @Pen.setter
    def Pen(self, value:'PdfPen'):
        GetDllLibPdf().PdfListItem_set_Pen.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfListItem_set_Pen(self.Ptr, value.Ptr)

    @property

    def Brush(self)->'PdfBrush':
        """
    <summary>
        Gets or sets list item brush.
    </summary>
        """
        GetDllLibPdf().PdfListItem_get_Brush.argtypes=[c_void_p]
        GetDllLibPdf().PdfListItem_get_Brush.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListItem_get_Brush(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @Brush.setter
    def Brush(self, value:'PdfBrush'):
        GetDllLibPdf().PdfListItem_set_Brush.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfListItem_set_Brush(self.Ptr, value.Ptr)

    @property

    def SubList(self)->'PdfListBase':
        """
    <summary>
        Gets or sets sublist for item. 
    </summary>
        """
        GetDllLibPdf().PdfListItem_get_SubList.argtypes=[c_void_p]
        GetDllLibPdf().PdfListItem_get_SubList.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListItem_get_SubList(self.Ptr)
        ret = None if intPtr==None else PdfListBase(intPtr)
        return ret


    @SubList.setter
    def SubList(self, value:'PdfListBase'):
        GetDllLibPdf().PdfListItem_set_SubList.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfListItem_set_SubList(self.Ptr, value.Ptr)

    @property
    def TextIndent(self)->float:
        """
    <summary>
        Gets or sets indent for item.
    </summary>
        """
        GetDllLibPdf().PdfListItem_get_TextIndent.argtypes=[c_void_p]
        GetDllLibPdf().PdfListItem_get_TextIndent.restype=c_float
        ret = GetDllLibPdf().PdfListItem_get_TextIndent(self.Ptr)
        return ret

    @TextIndent.setter
    def TextIndent(self, value:float):
        GetDllLibPdf().PdfListItem_set_TextIndent.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfListItem_set_TextIndent(self.Ptr, value)

