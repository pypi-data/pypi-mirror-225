from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfUriAnnotation (  PdfActionLinkAnnotation) :
    @dispatch
    def __init__(self,rectangle:RectangleF):
        ptrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfUriAnnotation_CreatePdfUriAnnotationR.argtypes=[c_void_p]
        GetDllLibPdf().PdfUriAnnotation_CreatePdfUriAnnotationR.restype = c_void_p
        intPtr = GetDllLibPdf().PdfUriAnnotation_CreatePdfUriAnnotationR(ptrrectangle)
        super(PdfUriAnnotation, self).__init__(intPtr)
    @dispatch
    def __init__(self,rectangle:RectangleF,uri:str):
        ptrrectangle:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfUriAnnotation_CreatePdfUriAnnotationRU.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfUriAnnotation_CreatePdfUriAnnotationRU.restype = c_void_p
        intPtr = GetDllLibPdf().PdfUriAnnotation_CreatePdfUriAnnotationRU(ptrrectangle,uri)
        super(PdfUriAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents the Uri annotation
    </summary>
    """
    @property

    def Uri(self)->str:
        """
    <summary>
        Gets or sets the Uri address.
    </summary>
        """
        GetDllLibPdf().PdfUriAnnotation_get_Uri.argtypes=[c_void_p]
        GetDllLibPdf().PdfUriAnnotation_get_Uri.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfUriAnnotation_get_Uri(self.Ptr))
        return ret


    @Uri.setter
    def Uri(self, value:str):
        GetDllLibPdf().PdfUriAnnotation_set_Uri.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfUriAnnotation_set_Uri(self.Ptr, value)

    @property

    def Action(self)->'PdfAction':
        """
    <summary>
        Gets or sets the action.
    </summary>
<value>The  object specifies the action of the annotation.</value>
        """
        GetDllLibPdf().PdfUriAnnotation_get_Action.argtypes=[c_void_p]
        GetDllLibPdf().PdfUriAnnotation_get_Action.restype=c_void_p
        intPtr = GetDllLibPdf().PdfUriAnnotation_get_Action(self.Ptr)
        ret = None if intPtr==None else PdfAction(intPtr)
        return ret


    @Action.setter
    def Action(self, value:'PdfAction'):
        GetDllLibPdf().PdfUriAnnotation_set_Action.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfUriAnnotation_set_Action(self.Ptr, value.Ptr)

