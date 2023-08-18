from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPopupAnnotationWidget (  PdfStyledAnnotationWidget) :
    """
    <summary>
        Represents the loaded pop up annotation class.
    </summary>
    """
    @property
    def Open(self)->bool:
        """
    <summary>
        Gets or sets the open option of the popup annotation.
    </summary>
        """
        GetDllLibPdf().PdfPopupAnnotationWidget_get_Open.argtypes=[c_void_p]
        GetDllLibPdf().PdfPopupAnnotationWidget_get_Open.restype=c_bool
        ret = GetDllLibPdf().PdfPopupAnnotationWidget_get_Open(self.Ptr)
        return ret

    @Open.setter
    def Open(self, value:bool):
        GetDllLibPdf().PdfPopupAnnotationWidget_set_Open.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfPopupAnnotationWidget_set_Open(self.Ptr, value)

    @property

    def Icon(self)->'PdfPopupIcon':
        """
    <summary>
        Gets or sets the icon of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfPopupAnnotationWidget_get_Icon.argtypes=[c_void_p]
        GetDllLibPdf().PdfPopupAnnotationWidget_get_Icon.restype=c_int
        ret = GetDllLibPdf().PdfPopupAnnotationWidget_get_Icon(self.Ptr)
        objwraped = PdfPopupIcon(ret)
        return objwraped

    @Icon.setter
    def Icon(self, value:'PdfPopupIcon'):
        GetDllLibPdf().PdfPopupAnnotationWidget_set_Icon.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPopupAnnotationWidget_set_Icon(self.Ptr, value.value)

    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfPopupAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfPopupAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfPopupAnnotationWidget_ObjectID(self.Ptr)
        return ret

