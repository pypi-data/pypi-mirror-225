from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfForm (SpireObject) :
    """
    <summary>
        Represents interactive form of the Pdf document.
    </summary>
    """
    @property

    def Fields(self)->'PdfFormFieldCollection':
        from spire.pdf.PdfFormFieldCollection import PdfFormFieldCollection
        """
    <summary>
        Gets the fields.
    </summary>
<value>The Form fields.</value>
        """
        GetDllLibPdf().PdfForm_get_Fields.argtypes=[c_void_p]
        GetDllLibPdf().PdfForm_get_Fields.restype=c_void_p
        intPtr = GetDllLibPdf().PdfForm_get_Fields(self.Ptr)
        ret = None if intPtr==None else PdfFormFieldCollection(intPtr)
        return ret


    @property
    def IsFlatten(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is flatten.
    </summary>
        """
        GetDllLibPdf().PdfForm_get_IsFlatten.argtypes=[c_void_p]
        GetDllLibPdf().PdfForm_get_IsFlatten.restype=c_bool
        ret = GetDllLibPdf().PdfForm_get_IsFlatten(self.Ptr)
        return ret

    @IsFlatten.setter
    def IsFlatten(self, value:bool):
        GetDllLibPdf().PdfForm_set_IsFlatten.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfForm_set_IsFlatten(self.Ptr, value)

    @property
    def ReadOnly(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether the form is read only.
    </summary>
<value>
  <c>true</c> if the form is read only; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfForm_get_ReadOnly.argtypes=[c_void_p]
        GetDllLibPdf().PdfForm_get_ReadOnly.restype=c_bool
        ret = GetDllLibPdf().PdfForm_get_ReadOnly(self.Ptr)
        return ret

    @ReadOnly.setter
    def ReadOnly(self, value:bool):
        GetDllLibPdf().PdfForm_set_ReadOnly.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfForm_set_ReadOnly(self.Ptr, value)

    @property
    def AutoNaming(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether [field auto naming].
    </summary>
        """
        GetDllLibPdf().PdfForm_get_AutoNaming.argtypes=[c_void_p]
        GetDllLibPdf().PdfForm_get_AutoNaming.restype=c_bool
        ret = GetDllLibPdf().PdfForm_get_AutoNaming(self.Ptr)
        return ret

    @AutoNaming.setter
    def AutoNaming(self, value:bool):
        GetDllLibPdf().PdfForm_set_AutoNaming.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfForm_set_AutoNaming(self.Ptr, value)

    @property
    def NeedAppearances(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether the viewer must generate appearances for fields.
    </summary>
<value>
  <c>true</c> if viewer must generate appearance; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfForm_get_NeedAppearances.argtypes=[c_void_p]
        GetDllLibPdf().PdfForm_get_NeedAppearances.restype=c_bool
        ret = GetDllLibPdf().PdfForm_get_NeedAppearances(self.Ptr)
        return ret

    @NeedAppearances.setter
    def NeedAppearances(self, value:bool):
        GetDllLibPdf().PdfForm_set_NeedAppearances.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfForm_set_NeedAppearances(self.Ptr, value)

