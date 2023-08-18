from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfUriAction (  PdfAction) :
    """
    <summary>
        Represents an action which resolves unique resource identifier.
    </summary>
    """
    @property

    def Uri(self)->str:
        """
    <summary>
        Gets or sets the unique resource identifier.
    </summary>
<value>The unique resource identifier.</value>
        """
        GetDllLibPdf().PdfUriAction_get_Uri.argtypes=[c_void_p]
        GetDllLibPdf().PdfUriAction_get_Uri.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfUriAction_get_Uri(self.Ptr))
        return ret


    @Uri.setter
    def Uri(self, value:str):
        GetDllLibPdf().PdfUriAction_set_Uri.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfUriAction_set_Uri(self.Ptr, value)

