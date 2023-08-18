from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfDestination (SpireObject) :
    @dispatch
    def __init__(self, page:PdfPageBase):
        ptrPage:c_void_p = page.Ptr
        GetDllLibPdf().PdfDestination_CreatePdfDestinationP.argtypes=[c_void_p]
        GetDllLibPdf().PdfDestination_CreatePdfDestinationP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDestination_CreatePdfDestinationP(ptrPage)
        super(PdfDestination, self).__init__(intPtr)

    @dispatch
    def __init__(self, page:PdfPageBase,location:PointF):
        ptrPage:c_void_p = page.Ptr
        ptrLocation:c_void_p = location.Ptr
        GetDllLibPdf().PdfDestination_CreatePdfDestinationPL.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfDestination_CreatePdfDestinationPL.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDestination_CreatePdfDestinationPL(ptrPage,ptrLocation)
        super(PdfDestination, self).__init__(intPtr)

    @dispatch
    def __init__(self, page:PdfPageBase,rectangle:RectangleF):
        ptrPage:c_void_p = page.Ptr
        ptrRec:c_void_p = rectangle.Ptr
        GetDllLibPdf().PdfDestination_CreatePdfDestinationPR.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfDestination_CreatePdfDestinationPR.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDestination_CreatePdfDestinationPR(ptrPage,ptrRec)
        super(PdfDestination, self).__init__(intPtr)

    @dispatch
    def __init__(self, pageNumber:int,location:PointF,zoom:float):
        ptrLocation:c_void_p = location.Ptr

        GetDllLibPdf().PdfDestination_CreatePdfDestinationPLZ.argtypes=[c_int,c_void_p,c_float]
        GetDllLibPdf().PdfDestination_CreatePdfDestinationPLZ.restype = c_void_p
        intPtr = GetDllLibPdf().PdfDestination_CreatePdfDestinationPLZ(pageNumber,ptrLocation,zoom)
        super(PdfDestination, self).__init__(intPtr)
    """
    <summary>
        Represents an anchor in the document where bookmarks or annotations can direct when clicked.
    </summary>
    """
    @property
    def PageNumber(self)->int:
        """
    <summary>
        The zero based page number.
    </summary>
        """
        GetDllLibPdf().PdfDestination_get_PageNumber.argtypes=[c_void_p]
        GetDllLibPdf().PdfDestination_get_PageNumber.restype=c_int
        ret = GetDllLibPdf().PdfDestination_get_PageNumber(self.Ptr)
        return ret

    @property
    def Zoom(self)->float:
        """
    <summary>
        Gets or sets zoom factor.
    </summary>
        """
        GetDllLibPdf().PdfDestination_get_Zoom.argtypes=[c_void_p]
        GetDllLibPdf().PdfDestination_get_Zoom.restype=c_float
        ret = GetDllLibPdf().PdfDestination_get_Zoom(self.Ptr)
        return ret

    @Zoom.setter
    def Zoom(self, value:float):
        GetDllLibPdf().PdfDestination_set_Zoom.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfDestination_set_Zoom(self.Ptr, value)

    @property

    def Page(self)->'PdfPageBase':
        """
    <summary>
        Gets or sets a page where the destination is situated.
    </summary>
        """
        GetDllLibPdf().PdfDestination_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().PdfDestination_get_Page.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDestination_get_Page(self.Ptr)
        ret = None if intPtr==None else PdfPageBase(intPtr)
        return ret


    @Page.setter
    def Page(self, value:'PdfPageBase'):
        GetDllLibPdf().PdfDestination_set_Page.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDestination_set_Page(self.Ptr, value.Ptr)

    @property

    def Mode(self)->'PdfDestinationMode':
        """
    <summary>
        Gets or sets mode of the destination.
    </summary>
        """
        GetDllLibPdf().PdfDestination_get_Mode.argtypes=[c_void_p]
        GetDllLibPdf().PdfDestination_get_Mode.restype=c_int
        ret = GetDllLibPdf().PdfDestination_get_Mode(self.Ptr)
        objwraped = PdfDestinationMode(ret)
        return objwraped

    @Mode.setter
    def Mode(self, value:'PdfDestinationMode'):
        GetDllLibPdf().PdfDestination_set_Mode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfDestination_set_Mode(self.Ptr, value.value)

    @property

    def Location(self)->'PointF':
        """
    <summary>
        Gets or sets a location of the destination.
    </summary>
        """
        GetDllLibPdf().PdfDestination_get_Location.argtypes=[c_void_p]
        GetDllLibPdf().PdfDestination_get_Location.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDestination_get_Location(self.Ptr)
        ret = None if intPtr==None else PointF(intPtr)
        return ret


    @Location.setter
    def Location(self, value:'PointF'):
        GetDllLibPdf().PdfDestination_set_Location.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDestination_set_Location(self.Ptr, value.Ptr)

    @property

    def Rectangle(self)->'RectangleF':
        """
    <summary>
        Gets or sets a rectangle of the destination.
    </summary>
        """
        GetDllLibPdf().PdfDestination_get_Rectangle.argtypes=[c_void_p]
        GetDllLibPdf().PdfDestination_get_Rectangle.restype=c_void_p
        intPtr = GetDllLibPdf().PdfDestination_get_Rectangle(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Rectangle.setter
    def Rectangle(self, value:'RectangleF'):
        GetDllLibPdf().PdfDestination_set_Rectangle.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfDestination_set_Rectangle(self.Ptr, value.Ptr)

    @property
    def IsValid(self)->bool:
        """
    <summary>
        Gets a value indicating whether this instance is valid.
    </summary>
<value>
  <c>true</c> if this instance is valid; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfDestination_get_IsValid.argtypes=[c_void_p]
        GetDllLibPdf().PdfDestination_get_IsValid.restype=c_bool
        ret = GetDllLibPdf().PdfDestination_get_IsValid(self.Ptr)
        return ret

