from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class BeginPageLayoutEventArgs (  PdfCancelEventArgs) :
    """
    <summary>
        Data for event before lay outing of the page.
    </summary>
    """
    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets or sets value that indicates the lay outing bounds on the page.
    </summary>
        """
        GetDllLibPdf().BeginPageLayoutEventArgs_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().BeginPageLayoutEventArgs_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().BeginPageLayoutEventArgs_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Bounds.setter
    def Bounds(self, value:'RectangleF'):
        GetDllLibPdf().BeginPageLayoutEventArgs_set_Bounds.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().BeginPageLayoutEventArgs_set_Bounds(self.Ptr, value.Ptr)

    @property

    def Page(self)->'PdfPageBase':
        """
    <summary>
        Gets the page where the lay outing should start.
    </summary>
        """
        GetDllLibPdf().BeginPageLayoutEventArgs_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().BeginPageLayoutEventArgs_get_Page.restype=c_void_p
        intPtr = GetDllLibPdf().BeginPageLayoutEventArgs_get_Page(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


