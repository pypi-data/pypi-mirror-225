from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfListWidgetItem (SpireObject) :
    """
    <summary>
        Represents loaded list item.
    </summary>
    """
    @dispatch
    def __init__(self, text:str, value:str):
        GetDllLibPdf().PdfListWidgetItem_CreatePdfListWidgetItemTV.argtypes=[c_wchar_p,c_wchar_p]
        GetDllLibPdf().PdfListWidgetItem_CreatePdfListWidgetItemTV.restype = c_void_p
        intPtr = GetDllLibPdf().PdfListWidgetItem_CreatePdfListWidgetItemTV(text,value)
        super(PdfListWidgetItem, self).__init__(intPtr)

    @property

    def Text(self)->str:
        """
    <summary>
        Gets or sets the text.
    </summary>
<value>A string value representing the display text of the item. </value>
        """
        GetDllLibPdf().PdfListWidgetItem_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfListWidgetItem_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfListWidgetItem_get_Text(self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        GetDllLibPdf().PdfListWidgetItem_set_Text.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfListWidgetItem_set_Text(self.Ptr, value)

    @property

    def Value(self)->str:
        """
    <summary>
        Gets or sets the value.
    </summary>
<value>A string value representing the value of the item. </value>
        """
        GetDllLibPdf().PdfListWidgetItem_get_Value.argtypes=[c_void_p]
        GetDllLibPdf().PdfListWidgetItem_get_Value.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfListWidgetItem_get_Value(self.Ptr))
        return ret


    @Value.setter
    def Value(self, value:str):
        GetDllLibPdf().PdfListWidgetItem_set_Value.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfListWidgetItem_set_Value(self.Ptr, value)

