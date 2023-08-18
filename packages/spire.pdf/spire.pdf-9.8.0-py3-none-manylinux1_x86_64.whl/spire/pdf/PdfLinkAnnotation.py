from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLinkAnnotation (  PdfAnnotation) :
    """
    <summary>
        Represents the base class for link annotations.
    </summary>
    """
    @property

    def HighlightMode(self)->'PdfHighlightMode':
        """

        """
        GetDllLibPdf().PdfLinkAnnotation_get_HighlightMode.argtypes=[c_void_p]
        GetDllLibPdf().PdfLinkAnnotation_get_HighlightMode.restype=c_int
        ret = GetDllLibPdf().PdfLinkAnnotation_get_HighlightMode(self.Ptr)
        objwraped = PdfHighlightMode(ret)
        return objwraped

    @HighlightMode.setter
    def HighlightMode(self, value:'PdfHighlightMode'):
        GetDllLibPdf().PdfLinkAnnotation_set_HighlightMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfLinkAnnotation_set_HighlightMode(self.Ptr, value.value)

