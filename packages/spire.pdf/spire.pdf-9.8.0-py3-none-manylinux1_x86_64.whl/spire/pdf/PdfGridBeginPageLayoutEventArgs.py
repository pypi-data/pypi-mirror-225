from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGridBeginPageLayoutEventArgs (  BeginPageLayoutEventArgs) :
    """
    <summary>
        Arguments of BeginPageLayoutEvent.
    </summary>
    """
    @property
    def StartRowIndex(self)->int:
        """
    <summary>
        Gets the start row.
    </summary>
<value>The start row.</value>
        """
        GetDllLibPdf().PdfGridBeginPageLayoutEventArgs_get_StartRowIndex.argtypes=[c_void_p]
        GetDllLibPdf().PdfGridBeginPageLayoutEventArgs_get_StartRowIndex.restype=c_int
        ret = GetDllLibPdf().PdfGridBeginPageLayoutEventArgs_get_StartRowIndex(self.Ptr)
        return ret

