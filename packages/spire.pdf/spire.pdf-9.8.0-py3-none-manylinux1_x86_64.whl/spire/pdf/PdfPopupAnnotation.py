from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfPopupAnnotation (  PdfAnnotation) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfPopupAnnotation_CreatePdfPopupAnnotation.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPopupAnnotation_CreatePdfPopupAnnotation()
        super(PdfPopupAnnotation, self).__init__(intPtr)
    @dispatch
    def __init__(self, rectangle:RectangleF):
        ptrRec:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfPopupAnnotation_CreatePdfPopupAnnotationR.argtypes=[c_void_p]
        GetDllLibPdf().PdfPopupAnnotation_CreatePdfPopupAnnotationR.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPopupAnnotation_CreatePdfPopupAnnotationR(ptrRec)
        super(PdfPopupAnnotation, self).__init__(intPtr)

    @dispatch
    def __init__(self, rectangle:RectangleF,text:str):
        ptrRec:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfPopupAnnotation_CreatePdfPopupAnnotationRT.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfPopupAnnotation_CreatePdfPopupAnnotationRT.restype = c_void_p
        intPtr = GetDllLibPdf().PdfPopupAnnotation_CreatePdfPopupAnnotationRT(ptrRec,text)
        super(PdfPopupAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents a Base class for popup annotation which can be either in open or closed state.
    </summary>
    """
    @property

    def Icon(self)->'PdfPopupIcon':
        """
    <summary>
        Gets or sets icon style.
    </summary>
        """
        GetDllLibPdf().PdfPopupAnnotation_get_Icon.argtypes=[c_void_p]
        GetDllLibPdf().PdfPopupAnnotation_get_Icon.restype=c_int
        ret = GetDllLibPdf().PdfPopupAnnotation_get_Icon(self.Ptr)
        objwraped = PdfPopupIcon(ret)
        return objwraped

    @Icon.setter
    def Icon(self, value:'PdfPopupIcon'):
        GetDllLibPdf().PdfPopupAnnotation_set_Icon.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfPopupAnnotation_set_Icon(self.Ptr, value.value)

    @property
    def Open(self)->bool:
        """
    <summary>
        Gets or sets value whether annotation is initially open or closed
    </summary>
        """
        GetDllLibPdf().PdfPopupAnnotation_get_Open.argtypes=[c_void_p]
        GetDllLibPdf().PdfPopupAnnotation_get_Open.restype=c_bool
        ret = GetDllLibPdf().PdfPopupAnnotation_get_Open(self.Ptr)
        return ret

    @Open.setter
    def Open(self, value:bool):
        GetDllLibPdf().PdfPopupAnnotation_set_Open.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfPopupAnnotation_set_Open(self.Ptr, value)

    @property

    def Appearance(self)->'PdfAppearance':
        """
    <summary>
        Gets or sets appearance of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfPopupAnnotation_get_Appearance.argtypes=[c_void_p]
        GetDllLibPdf().PdfPopupAnnotation_get_Appearance.restype=c_void_p
        intPtr = GetDllLibPdf().PdfPopupAnnotation_get_Appearance(self.Ptr)
        ret = None if intPtr==None else PdfAppearance(intPtr)
        return ret


    @Appearance.setter
    def Appearance(self, value:'PdfAppearance'):
        GetDllLibPdf().PdfPopupAnnotation_set_Appearance.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfPopupAnnotation_set_Appearance(self.Ptr, value.Ptr)

