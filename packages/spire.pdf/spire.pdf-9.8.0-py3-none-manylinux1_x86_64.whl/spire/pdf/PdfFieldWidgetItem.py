from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfFieldWidgetItem (SpireObject) :
    """
    <summary>
        Represents base class for field's group items.
    </summary>
    """
    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets or sets the bounds.
    </summary>
        """
        GetDllLibPdf().PdfFieldWidgetItem_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidgetItem_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFieldWidgetItem_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Bounds.setter
    def Bounds(self, value:'RectangleF'):
        GetDllLibPdf().PdfFieldWidgetItem_set_Bounds.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfFieldWidgetItem_set_Bounds(self.Ptr, value.Ptr)

    @property

    def Location(self)->'PointF':
        """
    <summary>
        Gets or sets the location.
    </summary>
        """
        GetDllLibPdf().PdfFieldWidgetItem_get_Location.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidgetItem_get_Location.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFieldWidgetItem_get_Location(self.Ptr)
        ret = None if intPtr==None else PointF(intPtr)
        return ret


    @Location.setter
    def Location(self, value:'PointF'):
        GetDllLibPdf().PdfFieldWidgetItem_set_Location.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfFieldWidgetItem_set_Location(self.Ptr, value.Ptr)

    @property

    def Size(self)->'SizeF':
        """
    <summary>
        Gets or sets the size.
    </summary>
        """
        GetDllLibPdf().PdfFieldWidgetItem_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidgetItem_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFieldWidgetItem_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @Size.setter
    def Size(self, value:'SizeF'):
        GetDllLibPdf().PdfFieldWidgetItem_set_Size.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfFieldWidgetItem_set_Size(self.Ptr, value.Ptr)

    @property

    def Page(self)->'PdfPageBase':
        """
    <summary>
        Gets the page.
    </summary>
        """
        GetDllLibPdf().PdfFieldWidgetItem_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().PdfFieldWidgetItem_get_Page.restype=c_void_p
        intPtr = GetDllLibPdf().PdfFieldWidgetItem_get_Page(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


