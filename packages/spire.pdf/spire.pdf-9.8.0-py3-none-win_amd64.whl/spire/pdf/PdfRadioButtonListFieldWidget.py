from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfRadioButtonListFieldWidget (  PdfStateFieldWidget) :
    """
    <summary>
        Represents radio button field of an existing PDF document`s form.
    </summary>
    """
    @property

    def WidgetWidgetItems(self)->'PdfRadioButtonWidgetWidgetItemCollection':
        """
    <summary>
        Gets the collection of radio button items.
    </summary>
<value>A  that represents the items within the list.</value>
        """
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_WidgetWidgetItems.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_WidgetWidgetItems.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadioButtonListFieldWidget_get_WidgetWidgetItems(self.Ptr)
        ret = None if intPtr==None else PdfRadioButtonWidgetWidgetItemCollection(intPtr)
        return ret


    @property
    def SelectedIndex(self)->int:
        """
    <summary>
        Gets or sets the index of the selected item in the list.
    </summary>
<value>The lowest ordinal index of the selected items in the list. The default is -1, which indicates that nothing is selected. </value>
        """
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_SelectedIndex.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_SelectedIndex.restype=c_int
        ret = GetDllLibPdf().PdfRadioButtonListFieldWidget_get_SelectedIndex(self.Ptr)
        return ret

    @SelectedIndex.setter
    def SelectedIndex(self, value:int):
        GetDllLibPdf().PdfRadioButtonListFieldWidget_set_SelectedIndex.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfRadioButtonListFieldWidget_set_SelectedIndex(self.Ptr, value)

    @property

    def SelectedValue(self)->str:
        """
    <summary>
        Gets or sets the value of the first selected item in the list. 
    </summary>
<value>A string value specifying the value of the first selected item, null (Nothing in VB.NET) if there is no selected item.</value>
        """
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_SelectedValue.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_SelectedValue.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfRadioButtonListFieldWidget_get_SelectedValue(self.Ptr))
        return ret


    @SelectedValue.setter
    def SelectedValue(self, value:str):
        GetDllLibPdf().PdfRadioButtonListFieldWidget_set_SelectedValue.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfRadioButtonListFieldWidget_set_SelectedValue(self.Ptr, value)

    @property

    def SelectedItem(self)->'PdfRadioButtonWidgetItem':
        """
    <summary>
        Gets the selected item.
    </summary>
<value>Return the item as PdfLoadedRadioButtonItem class</value>
        """
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_SelectedItem.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_SelectedItem.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRadioButtonListFieldWidget_get_SelectedItem(self.Ptr)
        ret = None if intPtr==None else PdfRadioButtonWidgetItem(intPtr)
        return ret


    @property

    def ButtonStyle(self)->'PdfCheckBoxStyle':
        """
    <summary>
        Gets the button style.
    </summary>
        """
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_ButtonStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_ButtonStyle.restype=c_int
        ret = GetDllLibPdf().PdfRadioButtonListFieldWidget_get_ButtonStyle(self.Ptr)
        objwraped = PdfCheckBoxStyle(ret)
        return objwraped

    @property

    def Value(self)->str:
        """
    <summary>
        Gets or sets the value of specified item.
    </summary>
<value>A string value representing the value of the item.</value>
        """
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_Value.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListFieldWidget_get_Value.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfRadioButtonListFieldWidget_get_Value(self.Ptr))
        return ret


    @Value.setter
    def Value(self, value:str):
        GetDllLibPdf().PdfRadioButtonListFieldWidget_set_Value.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfRadioButtonListFieldWidget_set_Value(self.Ptr, value)

    def ObjectID(self)->int:
        """
    <summary>
        Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfRadioButtonListFieldWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfRadioButtonListFieldWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfRadioButtonListFieldWidget_ObjectID(self.Ptr)
        return ret

