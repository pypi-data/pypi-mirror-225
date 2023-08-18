from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class SpotLocationType (SpireObject) :
    """
<remarks />
    """
    @property

    def PageURI(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().SpotLocationType_get_PageURI.argtypes=[c_void_p]
        GetDllLibPdf().SpotLocationType_get_PageURI.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().SpotLocationType_get_PageURI(self.Ptr))
        return ret


    @PageURI.setter
    def PageURI(self, value:str):
        GetDllLibPdf().SpotLocationType_set_PageURI.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().SpotLocationType_set_PageURI(self.Ptr, value)

    @property
    def StartX(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().SpotLocationType_get_StartX.argtypes=[c_void_p]
        GetDllLibPdf().SpotLocationType_get_StartX.restype=c_double
        ret = GetDllLibPdf().SpotLocationType_get_StartX(self.Ptr)
        return ret

    @StartX.setter
    def StartX(self, value:float):
        GetDllLibPdf().SpotLocationType_set_StartX.argtypes=[c_void_p, c_double]
        GetDllLibPdf().SpotLocationType_set_StartX(self.Ptr, value)

    @property
    def StartY(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().SpotLocationType_get_StartY.argtypes=[c_void_p]
        GetDllLibPdf().SpotLocationType_get_StartY.restype=c_double
        ret = GetDllLibPdf().SpotLocationType_get_StartY(self.Ptr)
        return ret

    @StartY.setter
    def StartY(self, value:float):
        GetDllLibPdf().SpotLocationType_set_StartY.argtypes=[c_void_p, c_double]
        GetDllLibPdf().SpotLocationType_set_StartY(self.Ptr, value)

