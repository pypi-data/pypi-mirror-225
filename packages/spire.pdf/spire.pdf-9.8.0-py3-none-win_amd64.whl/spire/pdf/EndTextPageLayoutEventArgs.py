from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class EndTextPageLayoutEventArgs (  EndPageLayoutEventArgs) :
    """
    <summary>
        Contains information about layout`s element .
    </summary>
    """
    @property

    def Result(self)->'PdfTextLayoutResult':
        """
    <summary>
        Gets a result of the lay outing on the page.
    </summary>
        """
        GetDllLibPdf().EndTextPageLayoutEventArgs_get_Result.argtypes=[c_void_p]
        GetDllLibPdf().EndTextPageLayoutEventArgs_get_Result.restype=c_void_p
        intPtr = GetDllLibPdf().EndTextPageLayoutEventArgs_get_Result(self.Ptr)
        ret = None if intPtr==None else PdfTextLayoutResult(intPtr)
        return ret


