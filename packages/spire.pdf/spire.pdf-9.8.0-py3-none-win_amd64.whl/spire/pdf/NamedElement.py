from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class NamedElement (SpireObject) :
    """
<remarks />
    """
    @property

    def NameReference(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().NamedElement_get_NameReference.argtypes=[c_void_p]
        GetDllLibPdf().NamedElement_get_NameReference.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().NamedElement_get_NameReference(self.Ptr))
        return ret


    @NameReference.setter
    def NameReference(self, value:str):
        GetDllLibPdf().NamedElement_set_NameReference.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().NamedElement_set_NameReference(self.Ptr, value)

