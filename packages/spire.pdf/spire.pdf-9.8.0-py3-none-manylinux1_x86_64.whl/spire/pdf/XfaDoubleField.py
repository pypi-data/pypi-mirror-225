from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XfaDoubleField (  XfaField) :
    """

    """
    @property
    def Value(self)->float:
        """

        """
        GetDllLibPdf().XfaDoubleField_get_Value.argtypes=[c_void_p]
        GetDllLibPdf().XfaDoubleField_get_Value.restype=c_double
        ret = GetDllLibPdf().XfaDoubleField_get_Value(self.Ptr)
        return ret

    @Value.setter
    def Value(self, value:float):
        GetDllLibPdf().XfaDoubleField_set_Value.argtypes=[c_void_p, c_double]
        GetDllLibPdf().XfaDoubleField_set_Value(self.Ptr, value)

