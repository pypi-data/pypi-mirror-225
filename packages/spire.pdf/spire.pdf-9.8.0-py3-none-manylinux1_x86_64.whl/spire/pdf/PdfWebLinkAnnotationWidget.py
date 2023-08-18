from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfWebLinkAnnotationWidget (  PdfUriAnnotationWidget) :
    """
    <summary>
        Represents the loaded web link annotation class.
    </summary>
    """
    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfWebLinkAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfWebLinkAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfWebLinkAnnotationWidget_ObjectID(self.Ptr)
        return ret

