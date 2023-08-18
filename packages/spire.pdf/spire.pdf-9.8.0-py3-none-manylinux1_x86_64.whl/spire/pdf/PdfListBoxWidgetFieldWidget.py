from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfListBoxWidgetFieldWidget (  PdfChoiceWidgetFieldWidget) :
    """
    <summary>
        Represents loaded list box field.
    </summary>
    """
    @property
    def MultiSelect(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether the field is multiselectable..
    </summary>
        """
        GetDllLibPdf().PdfListBoxWidgetFieldWidget_get_MultiSelect.argtypes=[c_void_p]
        GetDllLibPdf().PdfListBoxWidgetFieldWidget_get_MultiSelect.restype=c_bool
        ret = GetDllLibPdf().PdfListBoxWidgetFieldWidget_get_MultiSelect(self.Ptr)
        return ret

    @MultiSelect.setter
    def MultiSelect(self, value:bool):
        GetDllLibPdf().PdfListBoxWidgetFieldWidget_set_MultiSelect.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfListBoxWidgetFieldWidget_set_MultiSelect(self.Ptr, value)

    @property

    def Items(self)->'PdfListWidgetFieldItemCollection':
        """
    <summary>
        Gets the items.
    </summary>
<value>The collection of list box items.</value>
        """
        GetDllLibPdf().PdfListBoxWidgetFieldWidget_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().PdfListBoxWidgetFieldWidget_get_Items.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListBoxWidgetFieldWidget_get_Items(self.Ptr)
        ret = None if intPtr==None else PdfListWidgetFieldItemCollection(intPtr)
        return ret


    def ObjectID(self)->int:
        """
    <summary>
        Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfListBoxWidgetFieldWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfListBoxWidgetFieldWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfListBoxWidgetFieldWidget_ObjectID(self.Ptr)
        return ret

