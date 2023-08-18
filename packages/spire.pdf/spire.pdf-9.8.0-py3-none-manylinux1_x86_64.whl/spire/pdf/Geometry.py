from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Geometry (SpireObject) :
    """
<remarks />
    """
    @property

    def PathGeometry(self)->'PathGeometry':
        """
<remarks />
        """
        GetDllLibPdf().Geometry_get_PathGeometry.argtypes=[c_void_p]
        GetDllLibPdf().Geometry_get_PathGeometry.restype=c_void_p
        intPtr = GetDllLibPdf().Geometry_get_PathGeometry(self.Ptr)
        ret = None if intPtr==None else PathGeometry(intPtr)
        return ret


    @PathGeometry.setter
    def PathGeometry(self, value:'PathGeometry'):
        GetDllLibPdf().Geometry_set_PathGeometry.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Geometry_set_PathGeometry(self.Ptr, value.Ptr)

