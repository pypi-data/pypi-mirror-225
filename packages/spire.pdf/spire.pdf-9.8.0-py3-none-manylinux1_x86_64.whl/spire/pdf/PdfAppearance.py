from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAppearance (SpireObject) :
    @dispatch
    def __init__(self, annotation:PdfAnnotation):
        ptrAnno:c_void_p = annotation.Ptr
        GetDllLibPdf().PdfAppearance_CreatePdfAppearanceA.argtypes=[c_void_p]
        GetDllLibPdf().PdfAppearance_CreatePdfAppearanceA.restype = c_void_p
        intPtr = GetDllLibPdf().PdfAppearance_CreatePdfAppearanceA(ptrAnno)
        super(PdfAppearance, self).__init__(intPtr)
    """
    <summary>
        Represents the appearance of an annotation.
    </summary>
    """
    @property

    def Normal(self)->'PdfTemplate':
        """
    <summary>
        Gets or sets  object which applied to annotation in normal state.
    </summary>
        """
        GetDllLibPdf().PdfAppearance_get_Normal.argtypes=[c_void_p]
        GetDllLibPdf().PdfAppearance_get_Normal.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAppearance_get_Normal(self.Ptr)
        ret = None if intPtr==None else PdfTemplate(intPtr)
        return ret


    @Normal.setter
    def Normal(self, value:'PdfTemplate'):
        GetDllLibPdf().PdfAppearance_set_Normal.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAppearance_set_Normal(self.Ptr, value.Ptr)

    @property

    def MouseHover(self)->'PdfTemplate':
        """
    <summary>
        Gets or sets  object which applied to the annotation on hovering the mouse.
    </summary>
        """
        GetDllLibPdf().PdfAppearance_get_MouseHover.argtypes=[c_void_p]
        GetDllLibPdf().PdfAppearance_get_MouseHover.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAppearance_get_MouseHover(self.Ptr)
        ret = None if intPtr==None else PdfTemplate(intPtr)
        return ret


    @MouseHover.setter
    def MouseHover(self, value:'PdfTemplate'):
        GetDllLibPdf().PdfAppearance_set_MouseHover.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAppearance_set_MouseHover(self.Ptr, value.Ptr)

    @property

    def Pressed(self)->'PdfTemplate':
        """
    <summary>
        Gets or sets  object which applied to an annotation when mouse button is pressed.
    </summary>
        """
        GetDllLibPdf().PdfAppearance_get_Pressed.argtypes=[c_void_p]
        GetDllLibPdf().PdfAppearance_get_Pressed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAppearance_get_Pressed(self.Ptr)
        ret = None if intPtr==None else PdfTemplate(intPtr)
        return ret


    @Pressed.setter
    def Pressed(self, value:'PdfTemplate'):
        GetDllLibPdf().PdfAppearance_set_Pressed.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAppearance_set_Pressed(self.Ptr, value.Ptr)

