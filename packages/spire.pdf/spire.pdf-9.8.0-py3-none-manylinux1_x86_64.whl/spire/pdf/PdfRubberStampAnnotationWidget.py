from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfRubberStampAnnotationWidget (  PdfMarkUpAnnotationWidget) :
    """
    <summary>
        Represents the loaded rubber stamp annotation class.
    </summary>
    """
    @property

    def Icon(self)->'PdfRubberStampAnnotationIcon':
        """
    <summary>
        Gets or sets the icon of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfRubberStampAnnotationWidget_get_Icon.argtypes=[c_void_p]
        GetDllLibPdf().PdfRubberStampAnnotationWidget_get_Icon.restype=c_int
        ret = GetDllLibPdf().PdfRubberStampAnnotationWidget_get_Icon(self.Ptr)
        objwraped = PdfRubberStampAnnotationIcon(ret)
        return objwraped

    @Icon.setter
    def Icon(self, value:'PdfRubberStampAnnotationIcon'):
        GetDllLibPdf().PdfRubberStampAnnotationWidget_set_Icon.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfRubberStampAnnotationWidget_set_Icon(self.Ptr, value.value)

    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfRubberStampAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfRubberStampAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfRubberStampAnnotationWidget_ObjectID(self.Ptr)
        return ret

