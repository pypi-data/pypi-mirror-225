from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Transform (SpireObject) :
    """
<remarks />
    """
    @property

    def MatrixTransform(self)->'MatrixTransform':
        """
<remarks />
        """
        GetDllLibPdf().Transform_get_MatrixTransform.argtypes=[c_void_p]
        GetDllLibPdf().Transform_get_MatrixTransform.restype=c_void_p
        intPtr = GetDllLibPdf().Transform_get_MatrixTransform(self.Ptr)
        ret = None if intPtr==None else MatrixTransform(intPtr)
        return ret


    @MatrixTransform.setter
    def MatrixTransform(self, value:'MatrixTransform'):
        GetDllLibPdf().Transform_set_MatrixTransform.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Transform_set_MatrixTransform(self.Ptr, value.Ptr)

