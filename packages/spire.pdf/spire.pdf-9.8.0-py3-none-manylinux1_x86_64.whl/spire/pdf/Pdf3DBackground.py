from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DBackground (SpireObject) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().Pdf3DBackground_CreatePdf3DBackground.restype = c_void_p
        intPtr = GetDllLibPdf().Pdf3DBackground_CreatePdf3DBackground()
        super(Pdf3DBackground, self).__init__(intPtr)
    @dispatch
    def __init__(self, color:PdfRGBColor):
        ptrColor:c_void_p = color.Ptr
        GetDllLibPdf().Pdf3DBackground_CreatePdf3DBackgroundC.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DBackground_CreatePdf3DBackgroundC.restype = c_void_p
        intPtr = GetDllLibPdf().Pdf3DBackground_CreatePdf3DBackgroundC(ptrColor)
        super(Pdf3DBackground, self).__init__(intPtr)
    """
    <summary>
        Represents the background appearance for 3D artwork. 
    </summary>
    """
    @property

    def Color(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the background color.
    </summary>
<value>The  object specifying the background color for the 3D artwork. </value>
        """
        GetDllLibPdf().Pdf3DBackground_get_Color.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DBackground_get_Color.restype=c_void_p
        intPtr = GetDllLibPdf().Pdf3DBackground_get_Color(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @Color.setter
    def Color(self, value:'PdfRGBColor'):
        GetDllLibPdf().Pdf3DBackground_set_Color.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Pdf3DBackground_set_Color(self.Ptr, value.Ptr)

    @property
    def ApplyToEntireAnnotation(self)->bool:
        """
    <summary>
        Gets or sets a value indicating how the background is applied. 
    </summary>
<value>True if the background is applied to entire annotation, false if the background is applied to annotation's 3D view box only.</value>
        """
        GetDllLibPdf().Pdf3DBackground_get_ApplyToEntireAnnotation.argtypes=[c_void_p]
        GetDllLibPdf().Pdf3DBackground_get_ApplyToEntireAnnotation.restype=c_bool
        ret = GetDllLibPdf().Pdf3DBackground_get_ApplyToEntireAnnotation(self.Ptr)
        return ret

    @ApplyToEntireAnnotation.setter
    def ApplyToEntireAnnotation(self, value:bool):
        GetDllLibPdf().Pdf3DBackground_set_ApplyToEntireAnnotation.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().Pdf3DBackground_set_ApplyToEntireAnnotation(self.Ptr, value)

