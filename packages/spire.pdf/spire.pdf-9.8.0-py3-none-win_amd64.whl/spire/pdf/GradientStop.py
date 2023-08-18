from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class GradientStop (SpireObject) :
    """
<remarks />
    """
    @property

    def Color(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().GradientStop_get_Color.argtypes=[c_void_p]
        GetDllLibPdf().GradientStop_get_Color.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().GradientStop_get_Color(self.Ptr))
        return ret


    @Color.setter
    def Color(self, value:str):
        GetDllLibPdf().GradientStop_set_Color.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().GradientStop_set_Color(self.Ptr, value)

    @property
    def Offset(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().GradientStop_get_Offset.argtypes=[c_void_p]
        GetDllLibPdf().GradientStop_get_Offset.restype=c_double
        ret = GetDllLibPdf().GradientStop_get_Offset(self.Ptr)
        return ret

    @Offset.setter
    def Offset(self, value:float):
        GetDllLibPdf().GradientStop_set_Offset.argtypes=[c_void_p, c_double]
        GetDllLibPdf().GradientStop_set_Offset(self.Ptr, value)

