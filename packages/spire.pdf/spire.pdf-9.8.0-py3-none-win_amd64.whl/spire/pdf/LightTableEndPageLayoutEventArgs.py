from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class LightTableEndPageLayoutEventArgs (  EndPageLayoutEventArgs) :
    """

    """
    @property
    def StartRowIndex(self)->int:
        """

        """
        GetDllLibPdf().LightTableEndPageLayoutEventArgs_get_StartRowIndex.argtypes=[c_void_p]
        GetDllLibPdf().LightTableEndPageLayoutEventArgs_get_StartRowIndex.restype=c_int
        ret = GetDllLibPdf().LightTableEndPageLayoutEventArgs_get_StartRowIndex(self.Ptr)
        return ret

    @property
    def EndRowIndex(self)->int:
        """

        """
        GetDllLibPdf().LightTableEndPageLayoutEventArgs_get_EndRowIndex.argtypes=[c_void_p]
        GetDllLibPdf().LightTableEndPageLayoutEventArgs_get_EndRowIndex.restype=c_int
        ret = GetDllLibPdf().LightTableEndPageLayoutEventArgs_get_EndRowIndex(self.Ptr)
        return ret

