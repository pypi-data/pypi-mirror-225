from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfComboBoxWidgetFieldWidget (  PdfChoiceWidgetFieldWidget) :
    """
    <summary>
        Represents the combo box field of an existing item.
    </summary>
    """
    @property
    def Editable(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is editable.
    </summary>
<value>True if the drop down list is editable, false otherwise. Default is false.</value>
        """
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_get_Editable.argtypes=[c_void_p]
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_get_Editable.restype=c_bool
        ret = GetDllLibPdf().PdfComboBoxWidgetFieldWidget_get_Editable(self.Ptr)
        return ret

    @Editable.setter
    def Editable(self, value:bool):
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_set_Editable.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_set_Editable(self.Ptr, value)

    @property

    def WidgetItems(self)->'PdfComboBoxWidgetItemCollection':
        """
    <summary>
        Gets the collection of combo box items.
    </summary>
        """
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_get_WidgetItems.argtypes=[c_void_p]
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_get_WidgetItems.restype=c_void_p
        intPtr = GetDllLibPdf().PdfComboBoxWidgetFieldWidget_get_WidgetItems(self.Ptr)
        ret = None if intPtr==None else PdfComboBoxWidgetItemCollection(intPtr)
        return ret


    @property

    def SelectedValue(self)->str:
        """

        """
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_get_SelectedValue.argtypes=[c_void_p]
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_get_SelectedValue.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfComboBoxWidgetFieldWidget_get_SelectedValue(self.Ptr))
        return ret


    @SelectedValue.setter
    def SelectedValue(self, value:str):
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_set_SelectedValue.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_set_SelectedValue(self.Ptr, value)

    def ObjectID(self)->int:
        """
    <summary>
        Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfComboBoxWidgetFieldWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfComboBoxWidgetFieldWidget_ObjectID(self.Ptr)
        return ret

