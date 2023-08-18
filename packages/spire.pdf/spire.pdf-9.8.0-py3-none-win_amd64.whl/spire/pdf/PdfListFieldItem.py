from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfListFieldItem (SpireObject) :
    @dispatch
    def __init__(self, text:str, value:str):
        GetDllLibPdf().PdfListFieldItem_CreatePdfListFieldItemTV.argtypes=[c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfListFieldItem_CreatePdfListFieldItemTV.restype = c_void_p
        intPtr = GetDllLibPdf().PdfListFieldItem_CreatePdfListFieldItemTV(text,value)
        super(PdfListFieldItem, self).__init__(intPtr)
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfListFieldItem_CreatePdfListFieldItem.restype = c_void_p
        intPtr = GetDllLibPdf().PdfListFieldItem_CreatePdfListFieldItem()
        super(PdfListFieldItem, self).__init__(intPtr)
    """
    <summary>
        Represents an item of the list fields.
    </summary>
    """
    @property

    def Text(self)->str:
        """
    <summary>
        Gets or sets the text.
    </summary>
<value>The text of the list item field.</value>
        """
        GetDllLibPdf().PdfListFieldItem_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfListFieldItem_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfListFieldItem_get_Text(self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        GetDllLibPdf().PdfListFieldItem_set_Text.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfListFieldItem_set_Text(self.Ptr, value)

    @property

    def Value(self)->str:
        """
    <summary>
        Gets or sets the value.
    </summary>
<value>The value of the list item field.</value>
        """
        GetDllLibPdf().PdfListFieldItem_get_Value.argtypes=[c_void_p]
        GetDllLibPdf().PdfListFieldItem_get_Value.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfListFieldItem_get_Value(self.Ptr))
        return ret


    @Value.setter
    def Value(self, value:str):
        GetDllLibPdf().PdfListFieldItem_set_Value.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfListFieldItem_set_Value(self.Ptr, value)

