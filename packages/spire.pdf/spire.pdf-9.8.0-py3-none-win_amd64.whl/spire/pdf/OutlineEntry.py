from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class OutlineEntry (SpireObject) :
    """
<remarks />
    """
    @property
    def OutlineLevel(self)->int:
        """
<remarks />
        """
        GetDllLibPdf().OutlineEntry_get_OutlineLevel.argtypes=[c_void_p]
        GetDllLibPdf().OutlineEntry_get_OutlineLevel.restype=c_int
        ret = GetDllLibPdf().OutlineEntry_get_OutlineLevel(self.Ptr)
        return ret

    @OutlineLevel.setter
    def OutlineLevel(self, value:int):
        GetDllLibPdf().OutlineEntry_set_OutlineLevel.argtypes=[c_void_p, c_int]
        GetDllLibPdf().OutlineEntry_set_OutlineLevel(self.Ptr, value)

    @property

    def OutlineTarget(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().OutlineEntry_get_OutlineTarget.argtypes=[c_void_p]
        GetDllLibPdf().OutlineEntry_get_OutlineTarget.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().OutlineEntry_get_OutlineTarget(self.Ptr))
        return ret


    @OutlineTarget.setter
    def OutlineTarget(self, value:str):
        GetDllLibPdf().OutlineEntry_set_OutlineTarget.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().OutlineEntry_set_OutlineTarget(self.Ptr, value)

    @property

    def Description(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().OutlineEntry_get_Description.argtypes=[c_void_p]
        GetDllLibPdf().OutlineEntry_get_Description.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().OutlineEntry_get_Description(self.Ptr))
        return ret


    @Description.setter
    def Description(self, value:str):
        GetDllLibPdf().OutlineEntry_set_Description.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().OutlineEntry_set_Description(self.Ptr, value)

    @property

    def lang(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().OutlineEntry_get_lang.argtypes=[c_void_p]
        GetDllLibPdf().OutlineEntry_get_lang.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().OutlineEntry_get_lang(self.Ptr))
        return ret


    @lang.setter
    def lang(self, value:str):
        GetDllLibPdf().OutlineEntry_set_lang.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().OutlineEntry_set_lang(self.Ptr, value)

