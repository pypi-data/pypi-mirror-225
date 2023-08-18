from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextAnnotationWidget (  PdfMarkUpAnnotationWidget) :
    """

    """
    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfTextAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfTextAnnotationWidget_ObjectID(self.Ptr)
        return ret

