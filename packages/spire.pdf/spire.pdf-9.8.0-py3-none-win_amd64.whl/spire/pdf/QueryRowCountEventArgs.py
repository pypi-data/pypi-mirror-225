from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class QueryRowCountEventArgs (SpireObject) :
    """
    <summary>
        The arguments of the GettingRowNumber Event.
    </summary>
    """
    @property
    def RowCount(self)->int:
        """
    <summary>
        Gets or sets the column number.
    </summary>
        """
        GetDllLibPdf().QueryRowCountEventArgs_get_RowCount.argtypes=[c_void_p]
        GetDllLibPdf().QueryRowCountEventArgs_get_RowCount.restype=c_int
        ret = GetDllLibPdf().QueryRowCountEventArgs_get_RowCount(self.Ptr)
        return ret

    @RowCount.setter
    def RowCount(self, value:int):
        GetDllLibPdf().QueryRowCountEventArgs_set_RowCount.argtypes=[c_void_p, c_int]
        GetDllLibPdf().QueryRowCountEventArgs_set_RowCount(self.Ptr, value)

