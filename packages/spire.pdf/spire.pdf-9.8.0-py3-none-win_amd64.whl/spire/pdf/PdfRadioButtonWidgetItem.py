from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfRadioButtonWidgetItem (  PdfStateWidgetItem) :
    """
    <summary>
        Represents radio button field of an existing PDF document`s form.
    </summary>
    """
    @property

    def Value(self)->str:
        """
    <summary>
        Gets or sets the value.
    </summary>
<value>The value of the radio button item.</value>
        """
        GetDllLibPdf().PdfRadioButtonWidgetItem_get_Value.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonWidgetItem_get_Value.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfRadioButtonWidgetItem_get_Value(self.Ptr))
        return ret


    @Value.setter
    def Value(self, value:str):
        GetDllLibPdf().PdfRadioButtonWidgetItem_set_Value.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfRadioButtonWidgetItem_set_Value(self.Ptr, value)

    @property
    def Selected(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is selected.
    </summary>
        """
        GetDllLibPdf().PdfRadioButtonWidgetItem_get_Selected.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonWidgetItem_get_Selected.restype=c_bool
        ret = GetDllLibPdf().PdfRadioButtonWidgetItem_get_Selected(self.Ptr)
        return ret

    @Selected.setter
    def Selected(self, value:bool):
        GetDllLibPdf().PdfRadioButtonWidgetItem_set_Selected.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfRadioButtonWidgetItem_set_Selected(self.Ptr, value)

