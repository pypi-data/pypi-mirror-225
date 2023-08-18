from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextMarkupAnnotation (  PdfAnnotation) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotation.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotation()
        super(PdfTextMarkupAnnotation, self).__init__(intPtr)
    @dispatch
    def __init__(self, markupTitle:str , text:str, markupText:str, point:PointF , pdfFont:PdfFontBase):
        ptrP:c_void_p = point.Ptr
        ptrF:c_void_p = pdfFont.Ptr
        GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationMTMPP.argtypes=[c_wchar_p,c_wchar_p,c_wchar_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationMTMPP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationMTMPP(markupTitle,text,markupText,ptrP,ptrF)
        super(PdfTextMarkupAnnotation, self).__init__(intPtr)
    @dispatch
    def __init__(self, title:str , text:str, rect:RectangleF , pdfFont:PdfFontBase):
        ptrR:c_void_p = rect.Ptr
        ptrF:c_void_p = pdfFont.Ptr
        GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationTTRF.argtypes=[c_wchar_p,c_wchar_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationTTRF.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationTTRF(title,text,ptrR,ptrF)
        super(PdfTextMarkupAnnotation, self).__init__(intPtr)
    @dispatch
    def __init__(self, title:str , text:str, rect:RectangleF):
        ptrR:c_void_p = rect.Ptr
        GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationTTR.argtypes=[c_wchar_p,c_wchar_p,c_void_p]
        GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationTTR.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationTTR(title,text,ptrR)
        super(PdfTextMarkupAnnotation, self).__init__(intPtr)
    @dispatch
    def __init__(self, rect:RectangleF):
        ptrR:c_void_p = rect.Ptr
        GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationR.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationR.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTextMarkupAnnotation_CreatePdfTextMarkupAnnotationR(ptrR)
        super(PdfTextMarkupAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents the text markup annotation.
    </summary>
    """
    @property

    def TextMarkupAnnotationType(self)->'PdfTextMarkupAnnotationType':
        """
    <summary>
        Gets or sets TextMarkupAnnotationType .
    </summary>
        """
        GetDllLibPdf().PdfTextMarkupAnnotation_get_TextMarkupAnnotationType.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextMarkupAnnotation_get_TextMarkupAnnotationType.restype=c_int
        ret = GetDllLibPdf().PdfTextMarkupAnnotation_get_TextMarkupAnnotationType(self.Ptr)
        objwraped = PdfTextMarkupAnnotationType(ret)
        return objwraped

    @TextMarkupAnnotationType.setter
    def TextMarkupAnnotationType(self, value:'PdfTextMarkupAnnotationType'):
        GetDllLibPdf().PdfTextMarkupAnnotation_set_TextMarkupAnnotationType.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfTextMarkupAnnotation_set_TextMarkupAnnotationType(self.Ptr, value.value)

    @property

    def TextMarkupColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets text markup color.
    </summary>
        """
        GetDllLibPdf().PdfTextMarkupAnnotation_get_TextMarkupColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextMarkupAnnotation_get_TextMarkupColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTextMarkupAnnotation_get_TextMarkupColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @TextMarkupColor.setter
    def TextMarkupColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfTextMarkupAnnotation_set_TextMarkupColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfTextMarkupAnnotation_set_TextMarkupColor(self.Ptr, value.Ptr)

