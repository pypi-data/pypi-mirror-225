from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFileLinkAnnotation (  PdfActionLinkAnnotation) :
    @dispatch
    def __init__(self, rectangle:RectangleF,fileName:str):
        ptrRec:c_void_p = rectangle.Ptr
        GetDllLibPdf().PdfFileLinkAnnotation_CreatePdfFileLinkAnnotationRF.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfFileLinkAnnotation_CreatePdfFileLinkAnnotationRF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfFileLinkAnnotation_CreatePdfFileLinkAnnotationRF(ptrRec,fileName)
        super(PdfFileLinkAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents the annotation link to external file.
    </summary>
    """
    @property

    def FileName(self)->str:
        """
<value>A string value specifying the full path to the file to be embedded.</value>
        """
        GetDllLibPdf().PdfFileLinkAnnotation_get_FileName.argtypes=[c_void_p]
        GetDllLibPdf().PdfFileLinkAnnotation_get_FileName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfFileLinkAnnotation_get_FileName(self.Ptr))
        return ret


    @FileName.setter
    def FileName(self, value:str):
        GetDllLibPdf().PdfFileLinkAnnotation_set_FileName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfFileLinkAnnotation_set_FileName(self.Ptr, value)

    @property

    def Action(self)->'PdfAction':
        """
    <summary>
        Gets or sets the action.
    </summary>
<value>The action to be executed when the annotation is activated.</value>
        """
        GetDllLibPdf().PdfFileLinkAnnotation_get_Action.argtypes=[c_void_p]
        GetDllLibPdf().PdfFileLinkAnnotation_get_Action.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFileLinkAnnotation_get_Action(self.Ptr)
        ret = None if intPtr==None else PdfAction(intPtr)
        return ret


    @Action.setter
    def Action(self, value:'PdfAction'):
        GetDllLibPdf().PdfFileLinkAnnotation_set_Action.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfFileLinkAnnotation_set_Action(self.Ptr, value.Ptr)

