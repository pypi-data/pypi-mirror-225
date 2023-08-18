from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfBookmarkWidget (  PdfBookmark) :
    """
    <summary>
        Represents loaded bookmark class.
    </summary>
    """
    @property

    def Destination(self)->'PdfDestination':
        """
    <summary>
        Gets or sets the outline destination.
    </summary>
        """
        GetDllLibPdf().PdfBookmarkWidget_get_Destination.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmarkWidget_get_Destination.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBookmarkWidget_get_Destination(self.Ptr)
        ret = None if intPtr==None else PdfDestination(intPtr)
        return ret


    @Destination.setter
    def Destination(self, value:'PdfDestination'):
        GetDllLibPdf().PdfBookmarkWidget_set_Destination.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfBookmarkWidget_set_Destination(self.Ptr, value.Ptr)

    @property

    def Title(self)->str:
        """
    <summary>
        Gets or sets the outline title.
    </summary>
<remarks>The outline title is the text,
            which appears in the outline tree as a tree node.</remarks>
        """
        GetDllLibPdf().PdfBookmarkWidget_get_Title.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmarkWidget_get_Title.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfBookmarkWidget_get_Title(self.Ptr))
        return ret


    @Title.setter
    def Title(self, value:str):
        GetDllLibPdf().PdfBookmarkWidget_set_Title.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfBookmarkWidget_set_Title(self.Ptr, value)

    @property

    def Color(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the color.
    </summary>
        """
        GetDllLibPdf().PdfBookmarkWidget_get_Color.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmarkWidget_get_Color.restype=c_void_p
        intPtr = GetDllLibPdf().PdfBookmarkWidget_get_Color(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @Color.setter
    def Color(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfBookmarkWidget_set_Color.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfBookmarkWidget_set_Color(self.Ptr, value.Ptr)

    @property

    def DisplayStyle(self)->'PdfTextStyle':
        """
    <summary>
        Gets or sets the text style.
    </summary>
        """
        GetDllLibPdf().PdfBookmarkWidget_get_DisplayStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfBookmarkWidget_get_DisplayStyle.restype=c_int
        ret = GetDllLibPdf().PdfBookmarkWidget_get_DisplayStyle(self.Ptr)
        objwraped = PdfTextStyle(ret)
        return objwraped

    @DisplayStyle.setter
    def DisplayStyle(self, value:'PdfTextStyle'):
        GetDllLibPdf().PdfBookmarkWidget_set_DisplayStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfBookmarkWidget_set_DisplayStyle(self.Ptr, value.value)

