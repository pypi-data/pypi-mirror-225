from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfField (SpireObject) :
    """
    <summary>
        Represents field of the Pdf document's interactive form.
    </summary>
    """
    @property

    def Name(self)->str:
        """
    <summary>
        Gets the name.
    </summary>
<value>The name.</value>
        """
        GetDllLibPdf().PdfField_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().PdfField_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfField_get_Name(self.Ptr))
        return ret


    @property

    def FullName(self)->str:
        """

        """
        GetDllLibPdf().PdfField_get_FullName.argtypes=[c_void_p]
        GetDllLibPdf().PdfField_get_FullName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfField_get_FullName(self.Ptr))
        return ret


    @property

    def Form(self)->'PdfForm':
        """
    <summary>
        Gets the form.
    </summary>
<value>The form.</value>
        """
        GetDllLibPdf().PdfField_get_Form.argtypes=[c_void_p]
        GetDllLibPdf().PdfField_get_Form.restype=c_void_p
        intPtr = GetDllLibPdf().PdfField_get_Form(self.Ptr)
        ret = None if intPtr==None else PdfForm(intPtr)
        return ret


    @property

    def MappingName(self)->str:
        """
    <summary>
        Gets or sets the mapping name to be used when exporting interactive form 
            field data from the document.
    </summary>
<value>The mapping name.</value>
        """
        GetDllLibPdf().PdfField_get_MappingName.argtypes=[c_void_p]
        GetDllLibPdf().PdfField_get_MappingName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfField_get_MappingName(self.Ptr))
        return ret


    @MappingName.setter
    def MappingName(self, value:str):
        GetDllLibPdf().PdfField_set_MappingName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfField_set_MappingName(self.Ptr, value)

    @property
    def Export(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is export.
    </summary>
<value>
  <c>true</c> if export; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfField_get_Export.argtypes=[c_void_p]
        GetDllLibPdf().PdfField_get_Export.restype=c_bool
        ret = GetDllLibPdf().PdfField_get_Export(self.Ptr)
        return ret

    @Export.setter
    def Export(self, value:bool):
        GetDllLibPdf().PdfField_set_Export.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfField_set_Export(self.Ptr, value)

    @property
    def ReadOnly(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether [read only].
    </summary>
<value> if the field is read only, set to <c>true</c>.</value>
        """
        GetDllLibPdf().PdfField_get_ReadOnly.argtypes=[c_void_p]
        GetDllLibPdf().PdfField_get_ReadOnly.restype=c_bool
        ret = GetDllLibPdf().PdfField_get_ReadOnly(self.Ptr)
        return ret

    @ReadOnly.setter
    def ReadOnly(self, value:bool):
        GetDllLibPdf().PdfField_set_ReadOnly.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfField_set_ReadOnly(self.Ptr, value)

    @property
    def Required(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is required.
    </summary>
<value>
  <c>true</c> if required; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfField_get_Required.argtypes=[c_void_p]
        GetDllLibPdf().PdfField_get_Required.restype=c_bool
        ret = GetDllLibPdf().PdfField_get_Required(self.Ptr)
        return ret

    @Required.setter
    def Required(self, value:bool):
        GetDllLibPdf().PdfField_set_Required.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfField_set_Required(self.Ptr, value)

    @property

    def ToolTip(self)->str:
        """
    <summary>
        Gets or sets the tool tip.
    </summary>
<value>The tool tip.</value>
        """
        GetDllLibPdf().PdfField_get_ToolTip.argtypes=[c_void_p]
        GetDllLibPdf().PdfField_get_ToolTip.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfField_get_ToolTip(self.Ptr))
        return ret


    @ToolTip.setter
    def ToolTip(self, value:str):
        GetDllLibPdf().PdfField_set_ToolTip.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfField_set_ToolTip(self.Ptr, value)

    @property

    def Page(self)->'PdfPageBase':
        """
    <summary>
        Gets the page.
    </summary>
<value>The page.</value>
        """
        GetDllLibPdf().PdfField_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().PdfField_get_Page.restype=c_void_p
        intPtr = GetDllLibPdf().PdfField_get_Page(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @property
    def Flatten(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is flatten.
    </summary>
        """
        GetDllLibPdf().PdfField_get_Flatten.argtypes=[c_void_p]
        GetDllLibPdf().PdfField_get_Flatten.restype=c_bool
        ret = GetDllLibPdf().PdfField_get_Flatten(self.Ptr)
        return ret

    @Flatten.setter
    def Flatten(self, value:bool):
        GetDllLibPdf().PdfField_set_Flatten.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfField_set_Flatten(self.Ptr, value)

