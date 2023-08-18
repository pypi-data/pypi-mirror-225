from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfRadioButtonListField (  PdfField) :
    @dispatch
    def __init__(self, page:PdfPageBase,name:str):
        ptrPage:c_void_p = page.Ptr
        GetDllLibPdf().PdfRadioButtonListField_CreatePdfRadioButtonListFieldPN.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfRadioButtonListField_CreatePdfRadioButtonListFieldPN.restype = c_void_p
        intPtr = GetDllLibPdf().PdfRadioButtonListField_CreatePdfRadioButtonListFieldPN(ptrPage,name)
        super(PdfRadioButtonListField, self).__init__(intPtr)
    """
    <summary>
        Represents radio button field in the PDF form.
    </summary>
    """
    @property
    def SelectedIndex(self)->int:
        """
    <summary>
        Gets or sets the first selected item in the list. 
    </summary>
<value>The index of the selected item.</value>
        """
        GetDllLibPdf().PdfRadioButtonListField_get_SelectedIndex.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListField_get_SelectedIndex.restype=c_int
        ret = GetDllLibPdf().PdfRadioButtonListField_get_SelectedIndex(self.Ptr)
        return ret

    @SelectedIndex.setter
    def SelectedIndex(self, value:int):
        GetDllLibPdf().PdfRadioButtonListField_set_SelectedIndex.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfRadioButtonListField_set_SelectedIndex(self.Ptr, value)

    @property

    def SelectedValue(self)->str:
        """
    <summary>
        Gets or sets the value of the first selected item in the list.
    </summary>
<value>The selected value of the list field.</value>
        """
        GetDllLibPdf().PdfRadioButtonListField_get_SelectedValue.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListField_get_SelectedValue.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfRadioButtonListField_get_SelectedValue(self.Ptr))
        return ret


    @SelectedValue.setter
    def SelectedValue(self, value:str):
        GetDllLibPdf().PdfRadioButtonListField_set_SelectedValue.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfRadioButtonListField_set_SelectedValue(self.Ptr, value)

    @property

    def SelectedItem(self)->'PdfRadioButtonListItem':
        """
    <summary>
        Gets the first selected item in the list.
    </summary>
<value>The selected item of the field.</value>
        """
        GetDllLibPdf().PdfRadioButtonListField_get_SelectedItem.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListField_get_SelectedItem.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadioButtonListField_get_SelectedItem(self.Ptr)
        ret = None if intPtr==None else PdfRadioButtonListItem(intPtr)
        return ret


    @property

    def Items(self)->'PdfRadioButtonItemCollection':
        """
    <summary>
        Gets the items of the radio button field.
    </summary>
<value>The radio button field item collection.</value>
        """
        GetDllLibPdf().PdfRadioButtonListField_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListField_get_Items.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadioButtonListField_get_Items(self.Ptr)
        ret = None if intPtr==None else PdfRadioButtonItemCollection(intPtr)
        return ret


