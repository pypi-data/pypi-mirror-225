from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class QueryColumnCountEventArgs (SpireObject) :
    """
    <summary>
        The arguments of the GettingColumnNumber Event.
    </summary>
    """
    @property
    def ColumnCount(self)->int:
        """
    <summary>
        Gets or sets the column number.
    </summary>
        """
        GetDllLibPdf().QueryColumnCountEventArgs_get_ColumnCount.argtypes=[c_void_p]
        GetDllLibPdf().QueryColumnCountEventArgs_get_ColumnCount.restype=c_int
        ret = GetDllLibPdf().QueryColumnCountEventArgs_get_ColumnCount(self.Ptr)
        return ret

    @ColumnCount.setter
    def ColumnCount(self, value:int):
        GetDllLibPdf().QueryColumnCountEventArgs_set_ColumnCount.argtypes=[c_void_p, c_int]
        GetDllLibPdf().QueryColumnCountEventArgs_set_ColumnCount(self.Ptr, value)

