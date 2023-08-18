from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextMarkupAnnotationWidget (  PdfMarkUpAnnotationWidget) :
    """
    <summary>
        Represents the loaded text markup annotation class.
    </summary>
    """
    @property

    def TextMarkupAnnotationType(self)->'PdfTextMarkupAnnotationType':
        """
    <summary>
        Gets or sets the annotation Type.
    </summary>
        """
        GetDllLibPdf().PdfTextMarkupAnnotationWidget_get_TextMarkupAnnotationType.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextMarkupAnnotationWidget_get_TextMarkupAnnotationType.restype=c_int
        ret = GetDllLibPdf().PdfTextMarkupAnnotationWidget_get_TextMarkupAnnotationType(self.Ptr)
        objwraped = PdfTextMarkupAnnotationType(ret)
        return objwraped

    @TextMarkupAnnotationType.setter
    def TextMarkupAnnotationType(self, value:'PdfTextMarkupAnnotationType'):
        GetDllLibPdf().PdfTextMarkupAnnotationWidget_set_TextMarkupAnnotationType.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfTextMarkupAnnotationWidget_set_TextMarkupAnnotationType(self.Ptr, value.value)

    @property

    def TextMarkupColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the color.
    </summary>
        """
        GetDllLibPdf().PdfTextMarkupAnnotationWidget_get_TextMarkupColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextMarkupAnnotationWidget_get_TextMarkupColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTextMarkupAnnotationWidget_get_TextMarkupColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @TextMarkupColor.setter
    def TextMarkupColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfTextMarkupAnnotationWidget_set_TextMarkupColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfTextMarkupAnnotationWidget_set_TextMarkupColor(self.Ptr, value.Ptr)

    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfTextMarkupAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextMarkupAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfTextMarkupAnnotationWidget_ObjectID(self.Ptr)
        return ret

