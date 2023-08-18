from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAnnotationWidgetCollection (  PdfAnnotationCollection) :
    """
    <summary>
        Represents the loaded annotation colllection.
    </summary>
    """
    @dispatch

    def get_Item(self ,index:int)->PdfAnnotation:
        """
    <summary>
        Gets the  at the specified index.
    </summary>
        """
        
        GetDllLibPdf().PdfAnnotationWidgetCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().PdfAnnotationWidgetCollection_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAnnotationWidgetCollection_get_Item(self.Ptr, index)
        ret = None if intPtr==None else PdfAnnotation(intPtr)
        return ret


    @dispatch

    def get_Item(self ,text:str)->PdfAnnotation:
        """
    <summary>
        Represents the annotation with specified name.
    </summary>
    <param name="name">The specified annotation name.</param>
        """
        
        GetDllLibPdf().PdfAnnotationWidgetCollection_get_ItemT.argtypes=[c_void_p ,c_wchar_p]
        GetDllLibPdf().PdfAnnotationWidgetCollection_get_ItemT.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAnnotationWidgetCollection_get_ItemT(self.Ptr, text)
        ret = None if intPtr==None else PdfAnnotation(intPtr)
        return ret


    @property

    def PageWidget(self)->'PdfPageBase':
        """
    <summary>
        Gets or sets the page.
    </summary>
        """
        GetDllLibPdf().PdfAnnotationWidgetCollection_get_PageWidget.argtypes=[c_void_p]
        GetDllLibPdf().PdfAnnotationWidgetCollection_get_PageWidget.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAnnotationWidgetCollection_get_PageWidget(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @PageWidget.setter
    def PageWidget(self, value:'PdfPageBase'):
        GetDllLibPdf().PdfAnnotationWidgetCollection_set_PageWidget.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAnnotationWidgetCollection_set_PageWidget(self.Ptr, value.Ptr)


    def Add(self ,annotation:'PdfAnnotation')->int:
        """
    <summary>
        Adds annotation to collection.
    </summary>
    <param name="annotation">Annotation to be added to collection.</param>
    <returns>Position of the annotation in collection.</returns>
        """
        intPtrannotation:c_void_p = annotation.Ptr

        GetDllLibPdf().PdfAnnotationWidgetCollection_Add.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfAnnotationWidgetCollection_Add.restype=c_int
        ret = GetDllLibPdf().PdfAnnotationWidgetCollection_Add(self.Ptr, intPtrannotation)
        return ret

