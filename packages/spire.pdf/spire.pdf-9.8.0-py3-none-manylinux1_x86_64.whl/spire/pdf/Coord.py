from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Coord (SpireObject) :
    """

    """

    #def ToString(self)->str:
    #    """

    #    """
    #    GetDllLibPdf().Coord_ToString.argtypes=[c_void_p]
    #    GetDllLibPdf().Coord_ToString.restype=c_wchar_p
    #    ret = GetDllLibPdf().Coord_ToString(self.Ptr)
    #    return ret


    #def x(self)->int:
    #    """

    #    """
    #    GetDllLibPdf().Coord_x.argtypes=[c_void_p]
    #    GetDllLibPdf().Coord_x.restype=c_int
    #    ret = GetDllLibPdf().Coord_x(self.Ptr)
    #    return ret

    #def y(self)->int:
    #    """

    #    """
    #    GetDllLibPdf().Coord_y.argtypes=[c_void_p]
    #    GetDllLibPdf().Coord_y.restype=c_int
    #    ret = GetDllLibPdf().Coord_y(self.Ptr)
    #    return ret

