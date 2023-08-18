from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfLayoutWidget (  PdfGraphicsWidget) :
    """
    <summary>
        Represents the base class for all elements that can be layout on the pages.
    </summary>
            [System.Security.Permissions.PermissionSet(System.Security.Permissions.SecurityAction.Assert, Name = "FullTrust")]
        
    """

    def add_EndPageLayout(self ,value:'EndPageLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfLayoutWidget_add_EndPageLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfLayoutWidget_add_EndPageLayout(self.Ptr, intPtrvalue)


    def remove_EndPageLayout(self ,value:'EndPageLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfLayoutWidget_remove_EndPageLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfLayoutWidget_remove_EndPageLayout(self.Ptr, intPtrvalue)


    def add_BeginPageLayout(self ,value:'BeginPageLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfLayoutWidget_add_BeginPageLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfLayoutWidget_add_BeginPageLayout(self.Ptr, intPtrvalue)


    def remove_BeginPageLayout(self ,value:'BeginPageLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfLayoutWidget_remove_BeginPageLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfLayoutWidget_remove_BeginPageLayout(self.Ptr, intPtrvalue)
    
    @dispatch
    def Draw(self ,page,location:PointF)->PdfLayoutResult:
        """
    <summary>
        Draws the element on the page.
    </summary>
    <param name="page">Current page where the element should be drawn.</param>
    <param name="location">Start location on the page.</param>
    <returns>Layouting result.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlocation:c_void_p = location.Ptr

        GetDllLibPdf().PdfLayoutWidget_Draw.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfLayoutWidget_Draw.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayoutWidget_Draw(self.Ptr, intPtrpage,intPtrlocation)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page,x:float,y:float)->PdfLayoutResult:
        """
    <summary>
        Draws the element on the page.
    </summary>
    <param name="page">Current page where the element should be drawn.</param>
    <param name="x">X co-ordinate of the element on the page.</param>
    <param name="y">Y co-ordinate of the element on the page.</param>
    <returns>Lay outing result.</returns>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfLayoutWidget_DrawPXY.argtypes=[c_void_p ,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfLayoutWidget_DrawPXY.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayoutWidget_DrawPXY(self.Ptr, intPtrpage,x,y)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page,layoutRectangle:RectangleF)->PdfLayoutResult:
        """
    <summary>
        Draws the element on the page.
    </summary>
    <param name="page">Current page where the element should be drawn.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the element.</param>
    <returns>Lay outing result.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr

        GetDllLibPdf().PdfLayoutWidget_DrawPL.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfLayoutWidget_DrawPL.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayoutWidget_DrawPL(self.Ptr, intPtrpage,intPtrlayoutRectangle)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page,layoutRectangle:RectangleF,embedFonts:bool)->PdfLayoutResult:
        """
    <summary>
        Draws the element on the page.
    </summary>
    <param name="page">Current page where the element should be drawn.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the element.</param>
    <returns>Lay outing result.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr

        GetDllLibPdf().PdfLayoutWidget_DrawPLE.argtypes=[c_void_p ,c_void_p,c_void_p,c_bool]
        GetDllLibPdf().PdfLayoutWidget_DrawPLE.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayoutWidget_DrawPLE(self.Ptr, intPtrpage,intPtrlayoutRectangle,embedFonts)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page,location:PointF,format:PdfTextLayout)->PdfLayoutResult:
        """
    <summary>
        Draws the element on the page.
    </summary>
    <param name="page">Current page where the element should be drawn.</param>
    <param name="location">Start location on the page.</param>
    <param name="format">Lay outing format.</param>
    <returns>Lay outing result.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlocation:c_void_p = location.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfLayoutWidget_DrawPLF.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfLayoutWidget_DrawPLF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayoutWidget_DrawPLF(self.Ptr, intPtrpage,intPtrlocation,intPtrformat)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page,x:float,y:float,format:PdfTextLayout)->PdfLayoutResult:
        """
    <summary>
        Draws the element on the page.
    </summary>
    <param name="page">Current page where the element should be drawn.</param>
    <param name="x">X co-ordinate of the element on the page.</param>
    <param name="y">Y co-ordinate of the element on the page.</param>
    <param name="format">Layout format.</param>
    <returns>Layout result.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfLayoutWidget_DrawPXYF.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_void_p]
        GetDllLibPdf().PdfLayoutWidget_DrawPXYF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayoutWidget_DrawPXYF(self.Ptr, intPtrpage,x,y,intPtrformat)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page,layoutRectangle:RectangleF,format:PdfTextLayout)->PdfLayoutResult:
        """
    <summary>
        Draws the element on the page.
    </summary>
    <param name="page">Current page where the element should be drawn.</param>
    <param name="layoutRectangle">RectangleF structure that specifies the bounds of the element.</param>
    <param name="format">Layout format.</param>
    <returns>Layout result.</returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfLayoutWidget_DrawPLF1.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfLayoutWidget_DrawPLF1.restype=c_void_p
        intPtr = GetDllLibPdf().PdfLayoutWidget_DrawPLF1(self.Ptr, intPtrpage,intPtrlayoutRectangle,intPtrformat)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


