from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfMarkUpAnnotationWidget (  PdfStyledAnnotationWidget) :
    """
    <summary>
        Represents the loaded markup annotation class.
    </summary>
    """
    @property

    def Intent(self)->str:
        """
    <summary>
        Gets or sets the intent
    </summary>
        """
        GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Intent.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Intent.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Intent(self.Ptr))
        return ret


    @Intent.setter
    def Intent(self, value:str):
        GetDllLibPdf().PdfMarkUpAnnotationWidget_set_Intent.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfMarkUpAnnotationWidget_set_Intent(self.Ptr, value)

    @property

    def Author(self)->str:
        """
    <summary>
        Gets or sets the annotation's author.
    </summary>
        """
        GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Author.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Author.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Author(self.Ptr))
        return ret


    @Author.setter
    def Author(self, value:str):
        GetDllLibPdf().PdfMarkUpAnnotationWidget_set_Author.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfMarkUpAnnotationWidget_set_Author(self.Ptr, value)

    @property

    def CreationDate(self)->'DateTime':
        """
    <summary>
        Gets or sets the date and time when the annotation was created.
    </summary>
        """
        GetDllLibPdf().PdfMarkUpAnnotationWidget_get_CreationDate.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarkUpAnnotationWidget_get_CreationDate.restype=c_void_p
        intPtr = GetDllLibPdf().PdfMarkUpAnnotationWidget_get_CreationDate(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @CreationDate.setter
    def CreationDate(self, value:'DateTime'):
        GetDllLibPdf().PdfMarkUpAnnotationWidget_set_CreationDate.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfMarkUpAnnotationWidget_set_CreationDate(self.Ptr, value.Ptr)

    @property

    def Subject(self)->str:
        """
    <summary>
        Gets or sets the annotation's subject.
    </summary>
        """
        GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Subject.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Subject.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Subject(self.Ptr))
        return ret


    @Subject.setter
    def Subject(self, value:str):
        GetDllLibPdf().PdfMarkUpAnnotationWidget_set_Subject.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfMarkUpAnnotationWidget_set_Subject(self.Ptr, value)

    @property
    def Opacity(self)->float:
        """
    <summary>
        Gets the opacity value to be used.
    </summary>
        """
        GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Opacity.restype=c_float
        ret = GetDllLibPdf().PdfMarkUpAnnotationWidget_get_Opacity(self.Ptr)
        return ret


    def SetTitleText(self ,text:str):
        """
    <summary>
        Sets the name of the annotation,the entry is deleted by default when the input
            value is an empty string
    </summary>
    <param name="text">New name of the annotation.</param>
        """
        
        GetDllLibPdf().PdfMarkUpAnnotationWidget_SetTitleText.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfMarkUpAnnotationWidget_SetTitleText(self.Ptr, text)

    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfMarkUpAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfMarkUpAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfMarkUpAnnotationWidget_ObjectID(self.Ptr)
        return ret

