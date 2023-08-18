from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfResetAction (  PdfFormAction) :
    """
    <summary>
        Represents Pdf form's reset action.
    </summary>
<remarks>This action allows a user to reset the form fields to their default values. </remarks>
    """
    @property
    def Include(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether fields contained in Fields
            collection will be included for resetting.
    </summary>
<value>
  <c>true</c> if include; otherwise, <c>false</c>.</value>
<remarks>
            If Include property is true, only the fields in this collection will be reset.
            If Include property is false, the fields in this collection are not reset
            and only the remaining form fields are reset.
            If the collection is null or empty, then all the form fields are reset
            and the Include property is ignored.
            </remarks>
        """
        GetDllLibPdf().PdfResetAction_get_Include.argtypes=[c_void_p]
        GetDllLibPdf().PdfResetAction_get_Include.restype=c_bool
        ret = GetDllLibPdf().PdfResetAction_get_Include(self.Ptr)
        return ret

    @Include.setter
    def Include(self, value:bool):
        GetDllLibPdf().PdfResetAction_set_Include.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfResetAction_set_Include(self.Ptr, value)

