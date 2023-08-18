from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfDocumentLinkAnnotation (  PdfLinkAnnotation) :
    @dispatch
    def __init__(self, rectangle:RectangleF):
        ptrRec:c_void_p = rectangle.Ptr
        GetDllLibPdf().PdfDocumentLinkAnnotation_CreatePdfDocumentLinkAnnotationR.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentLinkAnnotation_CreatePdfDocumentLinkAnnotationR.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDocumentLinkAnnotation_CreatePdfDocumentLinkAnnotationR(ptrRec)
        super(PdfDocumentLinkAnnotation, self).__init__(intPtr)

    @dispatch
    def __init__(self, rectangle:RectangleF,destination:PdfDestination):
        ptrRec:c_void_p = rectangle.Ptr
        ptrDest:c_void_p = destination.Ptr
        GetDllLibPdf().PdfDocumentLinkAnnotation_CreatePdfDocumentLinkAnnotationRD.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfDocumentLinkAnnotation_CreatePdfDocumentLinkAnnotationRD.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDocumentLinkAnnotation_CreatePdfDocumentLinkAnnotationRD(ptrRec,ptrDest)
        super(PdfDocumentLinkAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents annotation object with holds link on another location within a document.
    </summary>
    """
    @property

    def Destination(self)->'PdfDestination':
        """
    <summary>
        Gets or sets the destination of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfDocumentLinkAnnotation_get_Destination.argtypes=[c_void_p]
        GetDllLibPdf().PdfDocumentLinkAnnotation_get_Destination.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDocumentLinkAnnotation_get_Destination(self.Ptr)
        ret = None if intPtr==None else PdfDestination(intPtr)
        return ret


    @Destination.setter
    def Destination(self, value:'PdfDestination'):
        GetDllLibPdf().PdfDocumentLinkAnnotation_set_Destination.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDocumentLinkAnnotation_set_Destination(self.Ptr, value.Ptr)

