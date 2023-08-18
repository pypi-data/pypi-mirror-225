from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFieldWidget (  PdfField) :
    """
    <summary>
        Represents base class for loaded fields.
    </summary>
    """
    @property

    def Name(self)->str:
        """
    <summary>
        Gets the name of the field.
    </summary>
<value>A string value specifying the name of the field.</value>
        """
        GetDllLibPdf().PdfFieldWidget_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidget_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfFieldWidget_get_Name(self.Ptr))
        return ret


    @property

    def MappingName(self)->str:
        """
    <summary>
        Gets or sets the mapping name to be used when exporting interactive form
            field data from the document.
    </summary>
<value>A string value specifying the mapping name of the field. </value>
        """
        GetDllLibPdf().PdfFieldWidget_get_MappingName.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidget_get_MappingName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfFieldWidget_get_MappingName(self.Ptr))
        return ret


    @MappingName.setter
    def MappingName(self, value:str):
        GetDllLibPdf().PdfFieldWidget_set_MappingName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfFieldWidget_set_MappingName(self.Ptr, value)

    @property

    def ToolTip(self)->str:
        """
    <summary>
        Gets or sets the tool tip.
    </summary>
        """
        GetDllLibPdf().PdfFieldWidget_get_ToolTip.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidget_get_ToolTip.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfFieldWidget_get_ToolTip(self.Ptr))
        return ret


    @ToolTip.setter
    def ToolTip(self, value:str):
        GetDllLibPdf().PdfFieldWidget_set_ToolTip.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfFieldWidget_set_ToolTip(self.Ptr, value)

    @property

    def Page(self)->'PdfPageBase':
        """
    <summary>
        Gets the page.
    </summary>
        """
        GetDllLibPdf().PdfFieldWidget_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidget_get_Page.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFieldWidget_get_Page(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @property
    def ReadOnly(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether [read only].
    </summary>
<value>True if the field is read-only, false otherwise. Default is false.</value>
        """
        GetDllLibPdf().PdfFieldWidget_get_ReadOnly.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidget_get_ReadOnly.restype=c_bool
        ret = GetDllLibPdf().PdfFieldWidget_get_ReadOnly(self.Ptr)
        return ret

    @ReadOnly.setter
    def ReadOnly(self, value:bool):
        GetDllLibPdf().PdfFieldWidget_set_ReadOnly.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfFieldWidget_set_ReadOnly(self.Ptr, value)

    @property
    def Required(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is required.
    </summary>
<value>True if the field is required, false otherwise. Default is false.</value>
        """
        GetDllLibPdf().PdfFieldWidget_get_Required.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidget_get_Required.restype=c_bool
        ret = GetDllLibPdf().PdfFieldWidget_get_Required(self.Ptr)
        return ret

    @Required.setter
    def Required(self, value:bool):
        GetDllLibPdf().PdfFieldWidget_set_Required.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfFieldWidget_set_Required(self.Ptr, value)

    @property
    def Export(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is export.
    </summary>
<value>
  <c>true</c> if export; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfFieldWidget_get_Export.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidget_get_Export.restype=c_bool
        ret = GetDllLibPdf().PdfFieldWidget_get_Export(self.Ptr)
        return ret

    @Export.setter
    def Export(self, value:bool):
        GetDllLibPdf().PdfFieldWidget_set_Export.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfFieldWidget_set_Export(self.Ptr, value)

    @property

    def FormWidget(self)->'PdfFormWidget':
        """
    <summary>
        Gets the form.
    </summary>
<value>The form.</value>
        """
        GetDllLibPdf().PdfFieldWidget_get_FormWidget.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidget_get_FormWidget.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFieldWidget_get_FormWidget(self.Ptr)
        ret = None if intPtr==None else PdfFormWidget(intPtr)
        return ret



    def ReSetPage(self ,page:'PdfPageBase'):
        """
    <summary>
        Re set the page.
    </summary>
    <param name="page">The page</param>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfFieldWidget_ReSetPage.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfFieldWidget_ReSetPage(self.Ptr, intPtrpage)


    def SetName(self ,name:str):
        """
    <summary>
        Sets the name of the field.
    </summary>
    <param name="name">New name of the field.</param>
        """
        
        GetDllLibPdf().PdfFieldWidget_SetName.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfFieldWidget_SetName(self.Ptr, name)

    def ObjectID(self)->int:
        """
    <summary>
        Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfFieldWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfFieldWidget_ObjectID(self.Ptr)
        return ret

