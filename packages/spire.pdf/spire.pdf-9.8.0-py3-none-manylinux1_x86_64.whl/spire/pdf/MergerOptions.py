from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class MergerOptions (SpireObject) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().MergerOptions_CreateMergerOptions.restype = c_void_p
        intPtr = GetDllLibPdf().MergerOptions_CreateMergerOptions()
        super(MergerOptions, self).__init__(intPtr)
    """
    <summary>
        The class can be used to set some options when do merge operation.
    </summary>
    """
    @property
    def SameFieldNameToOneField(self)->bool:
        """
    <summary>
        Gets or sets a value indicates whether to merge the fields with the same name into one field. 
    </summary>
        """
        GetDllLibPdf().MergerOptions_get_SameFieldNameToOneField.argtypes=[c_void_p]
        GetDllLibPdf().MergerOptions_get_SameFieldNameToOneField.restype=c_bool
        ret = GetDllLibPdf().MergerOptions_get_SameFieldNameToOneField(self.Ptr)
        return ret

    @SameFieldNameToOneField.setter
    def SameFieldNameToOneField(self, value:bool):
        GetDllLibPdf().MergerOptions_set_SameFieldNameToOneField.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().MergerOptions_set_SameFieldNameToOneField(self.Ptr, value)

