from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfComboBoxField (  PdfListField, IPdfComboBoxField) :
    @dispatch
    def __init__(self, page:PdfPageBase,name:str):
        ptrPage:c_void_p = page.Ptr
        GetDllLibPdf().PdfComboBoxField_CreatePdfComboBoxFieldPN.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfComboBoxField_CreatePdfComboBoxFieldPN.restype = c_void_p
        intPtr = GetDllLibPdf().PdfComboBoxField_CreatePdfComboBoxFieldPN(ptrPage,name)
        super(PdfComboBoxField, self).__init__(intPtr)
    """
    <summary>
        Represents combo box field in the PDF Form.
    </summary>
    """
    @property
    def Editable(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is editable.
    </summary>
<value>
  <c>true</c> if editable; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfComboBoxField_get_Editable.argtypes=[c_void_p]
        GetDllLibPdf().PdfComboBoxField_get_Editable.restype=c_bool
        ret = GetDllLibPdf().PdfComboBoxField_get_Editable(self.Ptr)
        return ret

    @Editable.setter
    def Editable(self, value:bool):
        GetDllLibPdf().PdfComboBoxField_set_Editable.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfComboBoxField_set_Editable(self.Ptr, value)

