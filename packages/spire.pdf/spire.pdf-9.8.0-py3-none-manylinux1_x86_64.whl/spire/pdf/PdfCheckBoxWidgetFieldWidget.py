from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCheckBoxWidgetFieldWidget (  PdfStateFieldWidget) :
    """
    <summary>
        Represents check box of an existing PDF document`s form. 
    </summary>
    """
    @property
    def Checked(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is checked.
    </summary>
<value>True if the check box is checked, false otherwise. </value>
        """
        GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_get_Checked.argtypes=[c_void_p]
        GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_get_Checked.restype=c_bool
        ret = GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_get_Checked(self.Ptr)
        return ret

    @Checked.setter
    def Checked(self, value:bool):
        GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_set_Checked.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_set_Checked(self.Ptr, value)

    @property

    def WidgetWidgetItems(self)->'PdfCheckBoxWidgetWidgetItemCollection':
        """
    <summary>
        Gets the collection check box items.
    </summary>
        """
        GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_get_WidgetWidgetItems.argtypes=[c_void_p]
        GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_get_WidgetWidgetItems.restype=c_void_p
        intPtr = GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_get_WidgetWidgetItems(self.Ptr)
        ret = None if intPtr==None else PdfCheckBoxWidgetWidgetItemCollection(intPtr)
        return ret



    def SetExportValue(self ,exportValue:str):
        """
    <summary>
        Set the export value.
    </summary>
    <param name="exportValue">The export value</param>
        """
        
        GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_SetExportValue.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_SetExportValue(self.Ptr, exportValue)

    def ObjectID(self)->int:
        """
    <summary>
        Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfCheckBoxWidgetFieldWidget_ObjectID(self.Ptr)
        return ret

