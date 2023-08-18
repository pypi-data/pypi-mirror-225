from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfCancelEventArgs (SpireObject) :
    """
    <summary>
        Represents the data for a cancelable event.
    </summary>
    """
    @property
    def Cancel(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is cancel.
    </summary>
<value>
  <c>true</c> if cancel; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfCancelEventArgs_get_Cancel.argtypes=[c_void_p]
        GetDllLibPdf().PdfCancelEventArgs_get_Cancel.restype=c_bool
        ret = GetDllLibPdf().PdfCancelEventArgs_get_Cancel(self.Ptr)
        return ret

    @Cancel.setter
    def Cancel(self, value:bool):
        GetDllLibPdf().PdfCancelEventArgs_set_Cancel.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfCancelEventArgs_set_Cancel(self.Ptr, value)

