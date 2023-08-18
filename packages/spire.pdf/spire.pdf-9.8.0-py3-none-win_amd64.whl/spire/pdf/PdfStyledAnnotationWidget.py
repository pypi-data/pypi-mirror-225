from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfStyledAnnotationWidget (  PdfAnnotationWidget) :
    """
    <summary>
        Represents the PdfLoadedStyledAnnotation.
    </summary>
    """
    @property

    def Color(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the color.
    </summary>
<value>The color.</value>
        """
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Color.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Color.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledAnnotationWidget_get_Color(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @Color.setter
    def Color(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Color.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Color(self.Ptr, value.Ptr)

    @property

    def Text(self)->str:
        """
    <summary>
        Gets or sets the text.
    </summary>
<value>The text.</value>
        """
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfStyledAnnotationWidget_get_Text(self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Text.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Text(self.Ptr, value)

    @property

    def Bounds(self)->'RectangleF':
        """

        """
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledAnnotationWidget_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Bounds.setter
    def Bounds(self, value:'RectangleF'):
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Bounds.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Bounds(self.Ptr, value.Ptr)

    @property

    def Border(self)->'PdfAnnotationBorder':
        """
    <summary>
        Gets or sets the annotation's border.
    </summary>
        """
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Border.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Border.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledAnnotationWidget_get_Border(self.Ptr)
        ret = None if intPtr==None else PdfAnnotationBorder(intPtr)
        return ret


    @Border.setter
    def Border(self, value:'PdfAnnotationBorder'):
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Border.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Border(self.Ptr, value.Ptr)

    @property

    def Location(self)->'PointF':
        """
    <summary>
        Gets or sets the location.
    </summary>
        """
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Location.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Location.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledAnnotationWidget_get_Location(self.Ptr)
        ret = None if intPtr==None else PointF(intPtr)
        return ret


    @Location.setter
    def Location(self, value:'PointF'):
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Location.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Location(self.Ptr, value.Ptr)

    @property

    def Size(self)->'SizeF':
        """
    <summary>
        Gets or sets the size.
    </summary>
        """
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledAnnotationWidget_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @Size.setter
    def Size(self, value:'SizeF'):
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Size.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_set_Size(self.Ptr, value.Ptr)

    @property

    def AnnotationFlags(self)->'PdfAnnotationFlags':
        """
    <summary>
        Gets or sets the annotation flags.
    </summary>
        """
        GetDllLibPdf().PdfStyledAnnotationWidget_get_AnnotationFlags.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_get_AnnotationFlags.restype=c_int
        ret = GetDllLibPdf().PdfStyledAnnotationWidget_get_AnnotationFlags(self.Ptr)
        objwraped = PdfAnnotationFlags(ret)
        return objwraped

    @AnnotationFlags.setter
    def AnnotationFlags(self, value:'PdfAnnotationFlags'):
        GetDllLibPdf().PdfStyledAnnotationWidget_set_AnnotationFlags.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfStyledAnnotationWidget_set_AnnotationFlags(self.Ptr, value.value)

    def ObjectID(self)->int:
        """
    <summary>
        Represents the Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfStyledAnnotationWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledAnnotationWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfStyledAnnotationWidget_ObjectID(self.Ptr)
        return ret

