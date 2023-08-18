from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPolyLineAnnotationWidget (  PdfPolygonAndPolyLineAnnotationWidget) :
    """
    <summary>
        Represents the loaded text Polygon annotation class.
    </summary>
    """
    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfPolyLineAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfPolyLineAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfPolyLineAnnotationWidget_ObjectID(self.Ptr)
        return ret

