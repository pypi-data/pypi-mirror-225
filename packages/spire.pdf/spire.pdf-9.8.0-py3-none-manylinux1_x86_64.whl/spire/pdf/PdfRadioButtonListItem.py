from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfRadioButtonListItem (  PdfCheckFieldBase) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfRadioButtonListItem_CreatePdfRadioButtonListItem.restype = c_void_p
        intPtr = GetDllLibPdf().PdfRadioButtonListItem_CreatePdfRadioButtonListItem()
        super(PdfRadioButtonListItem, self).__init__(intPtr)
    @dispatch
    def __init__(self, value:str):
        GetDllLibPdf().PdfRadioButtonListItem_CreatePdfRadioButtonListItemV.argtypes=[c_wchar_p]
        GetDllLibPdf().PdfRadioButtonListItem_CreatePdfRadioButtonListItemV.restype = c_void_p
        intPtr = GetDllLibPdf().PdfRadioButtonListItem_CreatePdfRadioButtonListItemV(value)
        super(PdfRadioButtonListItem, self).__init__(intPtr)
    """
    <summary>
        Represents an item of a radio button list.
    </summary>
    """
    @property

    def Form(self)->'PdfForm':
        """
    <summary>
        Gets the form of the field.
    </summary>
<value>The  object of the field.</value>
        """
        GetDllLibPdf().PdfRadioButtonListItem_get_Form.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListItem_get_Form.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadioButtonListItem_get_Form(self.Ptr)
        ret = None if intPtr==None else PdfForm(intPtr)
        return ret


    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets or sets the bounds.
    </summary>
        """
        GetDllLibPdf().PdfRadioButtonListItem_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListItem_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadioButtonListItem_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Bounds.setter
    def Bounds(self, value:'RectangleF'):
        GetDllLibPdf().PdfRadioButtonListItem_set_Bounds.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfRadioButtonListItem_set_Bounds(self.Ptr, value.Ptr)

    @property

    def Value(self)->str:
        """
    <summary>
        Gets or sets the value.
    </summary>
<value>The value.</value>
        """
        GetDllLibPdf().PdfRadioButtonListItem_get_Value.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListItem_get_Value.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfRadioButtonListItem_get_Value(self.Ptr))
        return ret


    @Value.setter
    def Value(self, value:str):
        GetDllLibPdf().PdfRadioButtonListItem_set_Value.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfRadioButtonListItem_set_Value(self.Ptr, value)

