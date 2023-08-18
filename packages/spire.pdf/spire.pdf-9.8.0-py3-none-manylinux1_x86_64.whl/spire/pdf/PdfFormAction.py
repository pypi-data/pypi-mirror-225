from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFormAction (  PdfAction) :
    """
    <summary>
        Represents the form action base class.
    </summary>
    """
    @property
    def Include(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether fields contained in  
            collection will be included for resetting or submitting.
    </summary>
<remarks>
            If Include property is true, only the fields in this collection will be reset or submitted.
            If Include property is false, the fields in this collection are not reset or submitted 
            and only the remaining form fields are reset or submitted.
            If the collection is null or empty, then all the form fields are reset 
            and the Include property is ignored.
            </remarks>
<value>
  <c>true</c> if include; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfFormAction_get_Include.argtypes=[c_void_p]
        GetDllLibPdf().PdfFormAction_get_Include.restype=c_bool
        ret = GetDllLibPdf().PdfFormAction_get_Include(self.Ptr)
        return ret

    @Include.setter
    def Include(self, value:bool):
        GetDllLibPdf().PdfFormAction_set_Include.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfFormAction_set_Include(self.Ptr, value)

    @property

    def Fields(self)->'PdfFieldCollection':
        """
    <summary>
        Gets the fields.
    </summary>
<value>The fields.</value>
        """
        GetDllLibPdf().PdfFormAction_get_Fields.argtypes=[c_void_p]
        GetDllLibPdf().PdfFormAction_get_Fields.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFormAction_get_Fields(self.Ptr)
        ret = None if intPtr==None else PdfFieldCollection(intPtr)
        return ret


