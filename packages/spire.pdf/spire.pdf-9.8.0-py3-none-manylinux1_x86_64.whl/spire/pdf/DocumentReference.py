from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class DocumentReference (SpireObject) :
    """
<remarks />
    """
    @property

    def Source(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().DocumentReference_get_Source.argtypes=[c_void_p]
        GetDllLibPdf().DocumentReference_get_Source.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocumentReference_get_Source(self.Ptr))
        return ret


    @Source.setter
    def Source(self, value:str):
        GetDllLibPdf().DocumentReference_set_Source.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocumentReference_set_Source(self.Ptr, value)

