from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFileLinkAnnotationWidget (  PdfStyledAnnotationWidget) :
    """
    <summary>
        Represents the loaded file link annotation class.
    </summary>
    """
    @property

    def FileName(self)->str:
        """
    <summary>
         Gets or sets the filename of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfFileLinkAnnotationWidget_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfFileLinkAnnotationWidget_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfFileLinkAnnotationWidget_get_FileName(self.Ptr))
        return ret


    @FileName.setter
    def FileName(self, value:str):
        GetDllLibPdf().PdfFileLinkAnnotationWidget_set_FileName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfFileLinkAnnotationWidget_set_FileName(self.Ptr, value)

    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfFileLinkAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfFileLinkAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfFileLinkAnnotationWidget_ObjectID(self.Ptr)
        return ret

