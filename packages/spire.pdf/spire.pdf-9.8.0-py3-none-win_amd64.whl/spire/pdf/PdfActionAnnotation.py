from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfActionAnnotation (  PdfActionLinkAnnotation) :
    @dispatch
    def __init__(self, rectangle:RectangleF,action:PdfAction):
        ptrRec:c_void_p = rectangle.Ptr
        ptrAction:c_void_p = action.Ptr

        GetDllLibPdf().PdfActionAnnotation_CreatePdfActionAnnotationRA.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfActionAnnotation_CreatePdfActionAnnotationRA.restype = c_void_p
        intPtr = GetDllLibPdf().PdfActionAnnotation_CreatePdfActionAnnotationRA(ptrRec,ptrAction)
        super(PdfActionAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents the annotation with associated action.
    </summary>
    """
