from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTemplate (  PdfShapeWidget) :
    @dispatch
    def __init__(self, size:SizeF):

        intPtrr:c_void_p = size.Ptr
        GetDllLibPdf().PdfTemplate_CreatePdfTemplateS.argtypes=[c_void_p]
        GetDllLibPdf().PdfTemplate_CreatePdfTemplateS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTemplate_CreatePdfTemplateS(intPtrr)
        super(PdfTemplate, self).__init__(intPtr)

    @dispatch
    def __init__(self, width:float,height:float):

        GetDllLibPdf().PdfTemplate_CreatePdfTemplateWH.argtypes=[c_float,c_float]
        GetDllLibPdf().PdfTemplate_CreatePdfTemplateWH.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTemplate_CreatePdfTemplateWH(width,height)
        super(PdfTemplate, self).__init__(intPtr)

    @dispatch
    def __init__(self, width:float,height:float,isPdfAppearance:bool):

        GetDllLibPdf().PdfTemplate_CreatePdfTemplateWHI.argtypes=[c_float,c_float,c_bool]
        GetDllLibPdf().PdfTemplate_CreatePdfTemplateWHI.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTemplate_CreatePdfTemplateWHI(width,height,isPdfAppearance)
        super(PdfTemplate, self).__init__(intPtr)
    """
    <summary>
        Represents Pdf Template object.
    </summary>
    """
    @property

    def Graphics(self)->'PdfCanvas':
        """
    <summary>
        Gets graphics context of the template.
    </summary>
<remarks>It will return null, if the template is read-only.</remarks>
        """
        GetDllLibPdf().PdfTemplate_get_Graphics.argtypes=[c_void_p]
        GetDllLibPdf().PdfTemplate_get_Graphics.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTemplate_get_Graphics(self.Ptr)
        ret = None if intPtr==None else PdfCanvas(intPtr)
        return ret


    @property

    def Size(self)->'SizeF':
        """
    <summary>
        Gets the size of the template.
    </summary>
        """
        GetDllLibPdf().PdfTemplate_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfTemplate_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTemplate_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @property
    def Width(self)->float:
        """
    <summary>
        Gets the width of the template.
    </summary>
        """
        GetDllLibPdf().PdfTemplate_get_Width.argtypes=[c_void_p]
        GetDllLibPdf().PdfTemplate_get_Width.restype=c_float
        ret = GetDllLibPdf().PdfTemplate_get_Width(self.Ptr)
        return ret

    @property
    def Height(self)->float:
        """
    <summary>
        Gets the height of the template.
    </summary>
        """
        GetDllLibPdf().PdfTemplate_get_Height.argtypes=[c_void_p]
        GetDllLibPdf().PdfTemplate_get_Height.restype=c_float
        ret = GetDllLibPdf().PdfTemplate_get_Height(self.Ptr)
        return ret

    @property
    def ReadOnly(self)->bool:
        """
    <summary>
        Gets a value indicating whether the template is read-only.
    </summary>
<value>
  <c>true</c> if the template is read-only; otherwise, <c>false</c>.</value>
<remarks>Read-only templates does not expose graphics. They just return null.</remarks>
        """
        GetDllLibPdf().PdfTemplate_get_ReadOnly.argtypes=[c_void_p]
        GetDllLibPdf().PdfTemplate_get_ReadOnly.restype=c_bool
        ret = GetDllLibPdf().PdfTemplate_get_ReadOnly(self.Ptr)
        return ret

    @dispatch

    def Reset(self ,size:SizeF):
        """
    <summary>
        Resets the template and sets the specified size.
    </summary>
    <param name="size">The size.</param>
        """
        intPtrsize:c_void_p = size.Ptr

        GetDllLibPdf().PdfTemplate_Reset.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfTemplate_Reset(self.Ptr, intPtrsize)

    @dispatch
    def Reset(self):
        """
    <summary>
        Resets an instance.
    </summary>
        """
        GetDllLibPdf().PdfTemplate_Reset1.argtypes=[c_void_p]
        GetDllLibPdf().PdfTemplate_Reset1(self.Ptr)

