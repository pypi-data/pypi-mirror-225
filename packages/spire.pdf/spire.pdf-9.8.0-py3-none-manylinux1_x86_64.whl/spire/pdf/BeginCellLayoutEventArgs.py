from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class BeginCellLayoutEventArgs (  CellLayoutEventArgs) :
    """
    <summary>
        Represents arguments of StartCellLayout Event.
    </summary>
    """
    @property
    def Skip(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether the value of this cell should be skipped.
    </summary>
        """
        GetDllLibPdf().BeginCellLayoutEventArgs_get_Skip.argtypes=[c_void_p]
        GetDllLibPdf().BeginCellLayoutEventArgs_get_Skip.restype=c_bool
        ret = GetDllLibPdf().BeginCellLayoutEventArgs_get_Skip(self.Ptr)
        return ret

    @Skip.setter
    def Skip(self, value:bool):
        GetDllLibPdf().BeginCellLayoutEventArgs_set_Skip.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().BeginCellLayoutEventArgs_set_Skip(self.Ptr, value)

