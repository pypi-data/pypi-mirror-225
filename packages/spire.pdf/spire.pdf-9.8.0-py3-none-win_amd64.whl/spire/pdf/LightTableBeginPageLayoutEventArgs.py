from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class LightTableBeginPageLayoutEventArgs (  BeginPageLayoutEventArgs) :
    """

    """
    @property
    def StartRowIndex(self)->int:
        """

        """
        GetDllLibPdf().LightTableBeginPageLayoutEventArgs_get_StartRowIndex.argtypes=[c_void_p]
        GetDllLibPdf().LightTableBeginPageLayoutEventArgs_get_StartRowIndex.restype=c_int
        ret = GetDllLibPdf().LightTableBeginPageLayoutEventArgs_get_StartRowIndex(self.Ptr)
        return ret

