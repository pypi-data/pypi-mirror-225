from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAnnotation (SpireObject) :
    """
    <summary>
        Represents the base class for annotation objects.
    </summary>
    """
    @property

    def Color(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the background of the annotations icon when closed.
            The title bar of the annotations pop-up window.
            The border of a link annotation.
    </summary>
<value>The color.</value>
        """
        GetDllLibPdf().PdfAnnotation_get_Color.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotation_get_Color.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAnnotation_get_Color(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @Color.setter
    def Color(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfAnnotation_set_Color.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAnnotation_set_Color(self.Ptr, value.Ptr)

    @property

    def ModifiedDate(self)->'DateTime':
        """
    <summary>
        Gets annotation's modified date.
    </summary>
        """
        GetDllLibPdf().PdfAnnotation_get_ModifiedDate.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotation_get_ModifiedDate.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAnnotation_get_ModifiedDate(self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @ModifiedDate.setter
    def ModifiedDate(self, value:'DateTime'):
        GetDllLibPdf().PdfAnnotation_set_ModifiedDate.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAnnotation_set_ModifiedDate(self.Ptr, value.Ptr)

    @property

    def Border(self)->'PdfAnnotationBorder':
        """
    <summary>
        Gets or sets annotation's border.
    </summary>
        """
        GetDllLibPdf().PdfAnnotation_get_Border.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotation_get_Border.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAnnotation_get_Border(self.Ptr)
        ret = None if intPtr==None else PdfAnnotationBorder(intPtr)
        return ret


    @Border.setter
    def Border(self, value:'PdfAnnotationBorder'):
        GetDllLibPdf().PdfAnnotation_set_Border.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAnnotation_set_Border(self.Ptr, value.Ptr)

    @property

    def Rectangle(self)->'RectangleF':
        """

        """
        GetDllLibPdf().PdfAnnotation_get_Rectangle.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotation_get_Rectangle.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAnnotation_get_Rectangle(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Rectangle.setter
    def Rectangle(self, value:'RectangleF'):
        GetDllLibPdf().PdfAnnotation_set_Rectangle.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAnnotation_set_Rectangle(self.Ptr, value.Ptr)

    @property

    def Location(self)->'PointF':
        """
    <summary>
        Gets or sets location of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfAnnotation_get_Location.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotation_get_Location.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAnnotation_get_Location(self.Ptr)
        ret = None if intPtr==None else PointF(intPtr)
        return ret


    @Location.setter
    def Location(self, value:'PointF'):
        GetDllLibPdf().PdfAnnotation_set_Location.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAnnotation_set_Location(self.Ptr, value.Ptr)

    @property

    def Name(self)->str:
        """
    <summary>
        Gets or sets the name of the annotation.
            Note: The annotation name, a text string uniquely identifying it among all the annotations on its page.
    </summary>
        """
        GetDllLibPdf().PdfAnnotation_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotation_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfAnnotation_get_Name(self.Ptr))
        return ret


    @Name.setter
    def Name(self, value:str):
        GetDllLibPdf().PdfAnnotation_set_Name.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfAnnotation_set_Name(self.Ptr, value)

    @property

    def Size(self)->'SizeF':
        """
    <summary>
        Gets or sets size of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfAnnotation_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotation_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAnnotation_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @Size.setter
    def Size(self, value:'SizeF'):
        GetDllLibPdf().PdfAnnotation_set_Size.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAnnotation_set_Size(self.Ptr, value.Ptr)

    @property

    #def Page(self)->'PdfPageBase':
    #    """
    #<summary>
    #    Gets a page which this annotation is connected to.
    #</summary>
    #    """
    #    GetDllLibPdf().PdfAnnotation_get_Page.argtypes=[c_void_p]
    #    GetDllLibPdf().PdfAnnotation_get_Page.restype=c_void_p
    #    intPtr = GetDllLibPdf().PdfAnnotation_get_Page(self.Ptr)
    #    ret = None if intPtr==None else PdfPageBase(intPtr)
    #    return ret


    @property

    def Text(self)->str:
        """
    <summary>
        Gets or sets content of the annotation.
    </summary>
        """
        GetDllLibPdf().PdfAnnotation_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotation_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfAnnotation_get_Text(self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        GetDllLibPdf().PdfAnnotation_set_Text.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfAnnotation_set_Text(self.Ptr, value)

    @property

    def Flags(self)->'PdfAnnotationFlags':
        """
    <summary>
        Gets or sets annotation flags.
    </summary>
        """
        GetDllLibPdf().PdfAnnotation_get_Flags.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotation_get_Flags.restype=c_int
        ret = GetDllLibPdf().PdfAnnotation_get_Flags(self.Ptr)
        objwraped = PdfAnnotationFlags(ret)
        return objwraped

    
    @Flags.setter
    def Flags(self, value:'PdfAnnotationFlags'):
        GetDllLibPdf().PdfAnnotation_set_Flags.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfAnnotation_set_Flags(self.Ptr, value.value)
    

    def pipeFlags(self, value:c_int):
        GetDllLibPdf().PdfAnnotation_set_Flags.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfAnnotation_set_Flags(self.Ptr, value)

