from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Discard (SpireObject) :
    """
<remarks />
    """
    @property

    def SentinelPage(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Discard_get_SentinelPage.argtypes=[c_void_p]
        GetDllLibPdf().Discard_get_SentinelPage.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Discard_get_SentinelPage(self.Ptr))
        return ret


    @SentinelPage.setter
    def SentinelPage(self, value:str):
        GetDllLibPdf().Discard_set_SentinelPage.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Discard_set_SentinelPage(self.Ptr, value)

    @property

    def Target(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Discard_get_Target.argtypes=[c_void_p]
        GetDllLibPdf().Discard_get_Target.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Discard_get_Target(self.Ptr))
        return ret


    @Target.setter
    def Target(self, value:str):
        GetDllLibPdf().Discard_set_Target.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Discard_set_Target(self.Ptr, value)

