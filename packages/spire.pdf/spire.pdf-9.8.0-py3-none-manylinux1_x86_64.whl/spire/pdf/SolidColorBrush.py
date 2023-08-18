from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class SolidColorBrush (SpireObject) :
    """
<remarks />
    """
    @property
    def Opacity(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().SolidColorBrush_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().SolidColorBrush_get_Opacity.restype=c_double
        ret = GetDllLibPdf().SolidColorBrush_get_Opacity(self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibPdf().SolidColorBrush_set_Opacity.argtypes=[c_void_p, c_double]
        GetDllLibPdf().SolidColorBrush_set_Opacity(self.Ptr, value)

    @property

    def Key(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().SolidColorBrush_get_Key.argtypes=[c_void_p]
        GetDllLibPdf().SolidColorBrush_get_Key.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().SolidColorBrush_get_Key(self.Ptr))
        return ret


    @Key.setter
    def Key(self, value:str):
        GetDllLibPdf().SolidColorBrush_set_Key.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().SolidColorBrush_set_Key(self.Ptr, value)

    @property

    def Color(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().SolidColorBrush_get_Color.argtypes=[c_void_p]
        GetDllLibPdf().SolidColorBrush_get_Color.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().SolidColorBrush_get_Color(self.Ptr))
        return ret


    @Color.setter
    def Color(self, value:str):
        GetDllLibPdf().SolidColorBrush_set_Color.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().SolidColorBrush_set_Color(self.Ptr, value)

