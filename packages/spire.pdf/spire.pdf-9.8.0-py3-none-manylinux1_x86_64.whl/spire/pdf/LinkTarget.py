from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class LinkTarget (SpireObject) :
    """
<remarks />
    """
    @property

    def Name(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().LinkTarget_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().LinkTarget_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().LinkTarget_get_Name(self.Ptr))
        return ret


    @Name.setter
    def Name(self, value:str):
        GetDllLibPdf().LinkTarget_set_Name.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().LinkTarget_set_Name(self.Ptr, value)

