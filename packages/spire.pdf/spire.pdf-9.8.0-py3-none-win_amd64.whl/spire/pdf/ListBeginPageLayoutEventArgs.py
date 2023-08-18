from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ListBeginPageLayoutEventArgs (  BeginPageLayoutEventArgs) :
    """

    """
    @property

    def List(self)->'PdfListBase':
        """

        """
        GetDllLibPdf().ListBeginPageLayoutEventArgs_get_List.argtypes=[c_void_p]
        GetDllLibPdf().ListBeginPageLayoutEventArgs_get_List.restype=c_void_p
        intPtr = GetDllLibPdf().ListBeginPageLayoutEventArgs_get_List(self.Ptr)
        ret = None if intPtr==None else PdfListBase(intPtr)
        return ret


