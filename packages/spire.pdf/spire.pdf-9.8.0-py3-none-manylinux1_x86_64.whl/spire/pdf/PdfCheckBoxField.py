from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCheckBoxField (  PdfCheckFieldBase) :
    @dispatch
    def __init__(self, page:PdfPageBase,name:str):
        ptrPage:c_void_p = page.Ptr
        GetDllLibPdf().PdfCheckBoxField_CreatePdfCheckBoxFieldPN.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfCheckBoxField_CreatePdfCheckBoxFieldPN.restype = c_void_p
        intPtr = GetDllLibPdf().PdfCheckBoxField_CreatePdfCheckBoxFieldPN(ptrPage,name)
        super(PdfCheckBoxField, self).__init__(intPtr)
    """
    <summary>
        Represents check box field in the PDF form.
    </summary>
    """
    @property
    def Checked(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is checked.
    </summary>
<value>
  <c>true</c> if checked; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfCheckBoxField_get_Checked.argtypes=[c_void_p]
        GetDllLibPdf().PdfCheckBoxField_get_Checked.restype=c_bool
        ret = GetDllLibPdf().PdfCheckBoxField_get_Checked(self.Ptr)
        return ret

    @Checked.setter
    def Checked(self, value:bool):
        GetDllLibPdf().PdfCheckBoxField_set_Checked.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfCheckBoxField_set_Checked(self.Ptr, value)

