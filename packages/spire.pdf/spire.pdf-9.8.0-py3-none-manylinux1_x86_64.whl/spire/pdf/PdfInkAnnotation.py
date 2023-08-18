from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfInkAnnotation (  PdfAnnotation) :
    """
    <summary>
        Represents Ink annotation in the PDF.
    </summary>
    """
#    @property
#
#    def InkList(self)->'List1':
#        """
#
#        """
#        GetDllLibPdf().PdfInkAnnotation_get_InkList.argtypes=[c_void_p]
#        GetDllLibPdf().PdfInkAnnotation_get_InkList.restype=c_void_p
#        intPtr = GetDllLibPdf().PdfInkAnnotation_get_InkList(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


#    @InkList.setter
#    def InkList(self, value:'List1'):
#        GetDllLibPdf().PdfInkAnnotation_set_InkList.argtypes=[c_void_p, c_void_p]
#        GetDllLibPdf().PdfInkAnnotation_set_InkList(self.Ptr, value.Ptr)


    @property
    def Opacity(self)->float:
        """
    <summary>
        Gets or sets the annotation opacity. 
            <remarks>The opacity is given in decimal, 1 is full opacity, 0 is no opacity.</remarks></summary>
        """
        GetDllLibPdf().PdfInkAnnotation_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().PdfInkAnnotation_get_Opacity.restype=c_float
        ret = GetDllLibPdf().PdfInkAnnotation_get_Opacity(self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibPdf().PdfInkAnnotation_set_Opacity.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfInkAnnotation_set_Opacity(self.Ptr, value)

