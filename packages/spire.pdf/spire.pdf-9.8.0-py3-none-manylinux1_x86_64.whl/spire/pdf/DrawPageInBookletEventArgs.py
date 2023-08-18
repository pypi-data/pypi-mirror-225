from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class DrawPageInBookletEventArgs (SpireObject) :
    """
    <summary>
        Represents DrawPageInBooklet Event arguments.
    </summary>
    """
    @property

    def PageInSource(self)->'PdfPageBase':
        """
    <summary>
        Gets the page of the source file.
    </summary>
        """
        GetDllLibPdf().DrawPageInBookletEventArgs_get_PageInSource.argtypes=[c_void_p]
        GetDllLibPdf().DrawPageInBookletEventArgs_get_PageInSource.restype=c_void_p
        intPtr = GetDllLibPdf().DrawPageInBookletEventArgs_get_PageInSource(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @property
    def PageNumberInSource(self)->int:
        """
    <summary>
        Gets the index of the source page, basing on 0.
    </summary>
        """
        GetDllLibPdf().DrawPageInBookletEventArgs_get_PageNumberInSource.argtypes=[c_void_p]
        GetDllLibPdf().DrawPageInBookletEventArgs_get_PageNumberInSource.restype=c_int
        ret = GetDllLibPdf().DrawPageInBookletEventArgs_get_PageNumberInSource(self.Ptr)
        return ret

    @property

    def PageInBooklet(self)->'PdfPageBase':
        """
    <summary>
        Gets the page of the booklet.
    </summary>
        """
        GetDllLibPdf().DrawPageInBookletEventArgs_get_PageInBooklet.argtypes=[c_void_p]
        GetDllLibPdf().DrawPageInBookletEventArgs_get_PageInBooklet.restype=c_void_p
        intPtr = GetDllLibPdf().DrawPageInBookletEventArgs_get_PageInBooklet(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @property
    def PageNumberInBooklet(self)->int:
        """
    <summary>
        Gets the index of the booklet page, basing on 0.
    </summary>
        """
        GetDllLibPdf().DrawPageInBookletEventArgs_get_PageNumberInBooklet.argtypes=[c_void_p]
        GetDllLibPdf().DrawPageInBookletEventArgs_get_PageNumberInBooklet.restype=c_int
        ret = GetDllLibPdf().DrawPageInBookletEventArgs_get_PageNumberInBooklet(self.Ptr)
        return ret

