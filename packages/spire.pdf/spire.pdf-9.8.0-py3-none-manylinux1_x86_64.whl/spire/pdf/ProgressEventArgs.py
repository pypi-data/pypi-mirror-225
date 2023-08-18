from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ProgressEventArgs (SpireObject) :
    """
    <summary>
        Shows the saving progress.
    </summary>
    """
    @property
    def Total(self)->int:
        """
    <summary>
        Gets the total number of the elements (pages) that need to be saved.
    </summary>
        """
        GetDllLibPdf().ProgressEventArgs_get_Total.argtypes=[c_void_p]
        GetDllLibPdf().ProgressEventArgs_get_Total.restype=c_int
        ret = GetDllLibPdf().ProgressEventArgs_get_Total(self.Ptr)
        return ret

    @property
    def Current(self)->int:
        """
    <summary>
        Gets the current element (page) index that just was saved.
    </summary>
<remarks>The index value increases constantly from 0 to Total.</remarks>
        """
        GetDllLibPdf().ProgressEventArgs_get_Current.argtypes=[c_void_p]
        GetDllLibPdf().ProgressEventArgs_get_Current.restype=c_int
        ret = GetDllLibPdf().ProgressEventArgs_get_Current(self.Ptr)
        return ret

    @property
    def Progress(self)->float:
        """
    <summary>
        Gets the progress.
    </summary>
<remarks>Progress constantly increases from 0.0 to 1.0.
            1.0 value means that entire document has been saved.</remarks>
        """
        GetDllLibPdf().ProgressEventArgs_get_Progress.argtypes=[c_void_p]
        GetDllLibPdf().ProgressEventArgs_get_Progress.restype=c_float
        ret = GetDllLibPdf().ProgressEventArgs_get_Progress(self.Ptr)
        return ret

