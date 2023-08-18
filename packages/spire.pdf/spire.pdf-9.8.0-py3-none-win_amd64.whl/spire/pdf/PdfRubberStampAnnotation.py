from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfRubberStampAnnotation (  PdfAnnotation) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfRubberStampAnnotation_CreatePdfRubberStampAnnotation.restype = c_void_p
        intPtr = GetDllLibPdf().PdfRubberStampAnnotation_CreatePdfRubberStampAnnotation()
        super(PdfRubberStampAnnotation, self).__init__(intPtr)
    @dispatch
    def __init__(self, rectangle:RectangleF):
        ptrRec:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfRubberStampAnnotation_CreatePdfRubberStampAnnotationR.argtypes=[c_void_p]
        GetDllLibPdf().PdfRubberStampAnnotation_CreatePdfRubberStampAnnotationR.restype = c_void_p
        intPtr = GetDllLibPdf().PdfRubberStampAnnotation_CreatePdfRubberStampAnnotationR(ptrRec)
        super(PdfRubberStampAnnotation, self).__init__(intPtr)

    @dispatch
    def __init__(self, rectangle:RectangleF,text:str):
        ptrRec:c_void_p = rectangle.Ptr

        GetDllLibPdf().PdfRubberStampAnnotation_CreatePdfRubberStampAnnotationRT.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfRubberStampAnnotation_CreatePdfRubberStampAnnotationRT.restype = c_void_p
        intPtr = GetDllLibPdf().PdfRubberStampAnnotation_CreatePdfRubberStampAnnotationRT(ptrRec,text)
        super(PdfRubberStampAnnotation, self).__init__(intPtr)
    """
    <summary>
        Represents the Rubber Stamp annotation for a PDF document.
    </summary>
    """
    @property

    def Icon(self)->'PdfRubberStampAnnotationIcon':
        """
    <summary>
        Gets or sets the annotation's icon. 
    </summary>
<value>A  enumeration member specifying the icon for the annotation when it is displayed in closed state. </value>
        """
        GetDllLibPdf().PdfRubberStampAnnotation_get_Icon.argtypes=[c_void_p]
        GetDllLibPdf().PdfRubberStampAnnotation_get_Icon.restype=c_int
        ret = GetDllLibPdf().PdfRubberStampAnnotation_get_Icon(self.Ptr)
        objwraped = PdfRubberStampAnnotationIcon(ret)
        return objwraped

    @Icon.setter
    def Icon(self, value:'PdfRubberStampAnnotationIcon'):
        GetDllLibPdf().PdfRubberStampAnnotation_set_Icon.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfRubberStampAnnotation_set_Icon(self.Ptr, value.value)

    @property

    def Appearance(self)->'PdfAppearance':
        """
    <summary>
        Gets or sets appearance of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfRubberStampAnnotation_get_Appearance.argtypes=[c_void_p]
        GetDllLibPdf().PdfRubberStampAnnotation_get_Appearance.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRubberStampAnnotation_get_Appearance(self.Ptr)
        ret = None if intPtr==None else PdfAppearance(intPtr)
        return ret


    @Appearance.setter
    def Appearance(self, value:'PdfAppearance'):
        GetDllLibPdf().PdfRubberStampAnnotation_set_Appearance.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfRubberStampAnnotation_set_Appearance(self.Ptr, value.Ptr)

    @property

    def Author(self)->str:
        """
    <summary>
        Gets or set the name of the annotation,the entry is deleted by default when the 
            input value is an empty string
    </summary>
        """
        GetDllLibPdf().PdfRubberStampAnnotation_get_Author.argtypes=[c_void_p]
        GetDllLibPdf().PdfRubberStampAnnotation_get_Author.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfRubberStampAnnotation_get_Author(self.Ptr))
        return ret


    @Author.setter
    def Author(self, value:str):
        GetDllLibPdf().PdfRubberStampAnnotation_set_Author.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfRubberStampAnnotation_set_Author(self.Ptr, value)

    @property

    def Subject(self)->str:
        """
    <summary>
        Gets or sets the annotation's subject.
    </summary>
        """
        GetDllLibPdf().PdfRubberStampAnnotation_get_Subject.argtypes=[c_void_p]
        GetDllLibPdf().PdfRubberStampAnnotation_get_Subject.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfRubberStampAnnotation_get_Subject(self.Ptr))
        return ret


    @Subject.setter
    def Subject(self, value:str):
        GetDllLibPdf().PdfRubberStampAnnotation_set_Subject.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfRubberStampAnnotation_set_Subject(self.Ptr, value)

    @property

    def CreationDate(self)->'DateTime':
        """
    <summary>
        Gets or sets the creation date.
    </summary>
        """
        GetDllLibPdf().PdfRubberStampAnnotation_get_CreationDate.argtypes=[c_void_p]
        GetDllLibPdf().PdfRubberStampAnnotation_get_CreationDate.restype=c_void_p
        intPtr = GetDllLibPdf().PdfRubberStampAnnotation_get_CreationDate(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @CreationDate.setter
    def CreationDate(self, value:'DateTime'):
        GetDllLibPdf().PdfRubberStampAnnotation_set_CreationDate.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfRubberStampAnnotation_set_CreationDate(self.Ptr, value.Ptr)

