from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFreeTextAnnotation (  PdfAnnotation) :
    @dispatch
    def __init__(self, rectangle:RectangleF):
        ptrRec:c_void_p = rectangle.Ptr
        GetDllLibPdf().PdfFreeTextAnnotation_CreatePdfFreeTextAnnotationR.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_CreatePdfFreeTextAnnotationR.restype = c_void_p
        intPtr = GetDllLibPdf().PdfFreeTextAnnotation_CreatePdfFreeTextAnnotationR(ptrRec)
        super(PdfFreeTextAnnotation, self).__init__(intPtr)
    """

    """
    @property

    def LineEndingStyle(self)->'PdfLineEndingStyle':
        """

        """
        GetDllLibPdf().PdfFreeTextAnnotation_get_LineEndingStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_get_LineEndingStyle.restype=c_int
        ret = GetDllLibPdf().PdfFreeTextAnnotation_get_LineEndingStyle(self.Ptr)
        objwraped = PdfLineEndingStyle(ret)
        return objwraped

    @LineEndingStyle.setter
    def LineEndingStyle(self, value:'PdfLineEndingStyle'):
        GetDllLibPdf().PdfFreeTextAnnotation_set_LineEndingStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfFreeTextAnnotation_set_LineEndingStyle(self.Ptr, value.value)

    @property

    def AnnotationIntent(self)->'PdfAnnotationIntent':
        """

        """
        GetDllLibPdf().PdfFreeTextAnnotation_get_AnnotationIntent.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_get_AnnotationIntent.restype=c_int
        ret = GetDllLibPdf().PdfFreeTextAnnotation_get_AnnotationIntent(self.Ptr)
        objwraped = PdfAnnotationIntent(ret)
        return objwraped

    @AnnotationIntent.setter
    def AnnotationIntent(self, value:'PdfAnnotationIntent'):
        GetDllLibPdf().PdfFreeTextAnnotation_set_AnnotationIntent.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfFreeTextAnnotation_set_AnnotationIntent(self.Ptr, value.value)

    @property

    def MarkupText(self)->str:
        """

        """
        GetDllLibPdf().PdfFreeTextAnnotation_get_MarkupText.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_get_MarkupText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfFreeTextAnnotation_get_MarkupText(self.Ptr))
        return ret


    @MarkupText.setter
    def MarkupText(self, value:str):
        GetDllLibPdf().PdfFreeTextAnnotation_set_MarkupText.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfFreeTextAnnotation_set_MarkupText(self.Ptr, value)

    @property
    def Opacity(self)->float:
        """

        """
        GetDllLibPdf().PdfFreeTextAnnotation_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_get_Opacity.restype=c_float
        ret = GetDllLibPdf().PdfFreeTextAnnotation_get_Opacity(self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibPdf().PdfFreeTextAnnotation_set_Opacity.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfFreeTextAnnotation_set_Opacity(self.Ptr, value)

    @property

    def Font(self)->'PdfFontBase':
        """

        """
        GetDllLibPdf().PdfFreeTextAnnotation_get_Font.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_get_Font.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFreeTextAnnotation_get_Font(self.Ptr)
        ret = None if intPtr==None else PdfFontBase(intPtr)
        return ret


    @Font.setter
    def Font(self, value:'PdfFontBase'):
        GetDllLibPdf().PdfFreeTextAnnotation_set_Font.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_set_Font(self.Ptr, value.Ptr)

    @property

    def CalloutLines(self)->List['PointF']:
        """

        """
        GetDllLibPdf().PdfFreeTextAnnotation_get_CalloutLines.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_get_CalloutLines.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfFreeTextAnnotation_get_CalloutLines(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, PointF)
        return ret


    @CalloutLines.setter
    def CalloutLines(self, value:List['PointF']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().PdfFreeTextAnnotation_set_CalloutLines.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfFreeTextAnnotation_set_CalloutLines(self.Ptr, vArray, vCount)


    @property

    def TextMarkupColor(self)->'PdfRGBColor':
        """

        """
        GetDllLibPdf().PdfFreeTextAnnotation_get_TextMarkupColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_get_TextMarkupColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFreeTextAnnotation_get_TextMarkupColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @TextMarkupColor.setter
    def TextMarkupColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfFreeTextAnnotation_set_TextMarkupColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_set_TextMarkupColor(self.Ptr, value.Ptr)

    @property

    def BorderColor(self)->'PdfRGBColor':
        """

        """
        GetDllLibPdf().PdfFreeTextAnnotation_get_BorderColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_get_BorderColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFreeTextAnnotation_get_BorderColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @BorderColor.setter
    def BorderColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfFreeTextAnnotation_set_BorderColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_set_BorderColor(self.Ptr, value.Ptr)

    @property

    def RectangleDifferences(self)->List[float]:
        """
    <summary>
        Gets or sets the rectangular diffecences
    </summary>
        """
        GetDllLibPdf().PdfFreeTextAnnotation_get_RectangleDifferences.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_get_RectangleDifferences.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfFreeTextAnnotation_get_RectangleDifferences(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, c_float)
        return ret

    @RectangleDifferences.setter
    def RectangleDifferences(self, value:List[float]):
        vCount = len(value)
        ArrayType = c_float * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i]
        GetDllLibPdf().PdfFreeTextAnnotation_set_RectangleDifferences.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfFreeTextAnnotation_set_RectangleDifferences(self.Ptr, vArray, vCount)

    @property

    def Author(self)->str:
        """
    <summary>
        Gets or sets the user who created the annotation.
    </summary>
        """
        GetDllLibPdf().PdfFreeTextAnnotation_get_Author.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_get_Author.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfFreeTextAnnotation_get_Author(self.Ptr))
        return ret


    @Author.setter
    def Author(self, value:str):
        GetDllLibPdf().PdfFreeTextAnnotation_set_Author.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfFreeTextAnnotation_set_Author(self.Ptr, value)

    @property

    def Subject(self)->str:
        """
    <summary>
        Gets or sets the annotation's subject.
    </summary>
        """
        GetDllLibPdf().PdfFreeTextAnnotation_get_Subject.argtypes=[c_void_p]
        GetDllLibPdf().PdfFreeTextAnnotation_get_Subject.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfFreeTextAnnotation_get_Subject(self.Ptr))
        return ret


    @Subject.setter
    def Subject(self, value:str):
        GetDllLibPdf().PdfFreeTextAnnotation_set_Subject.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfFreeTextAnnotation_set_Subject(self.Ptr, value)

