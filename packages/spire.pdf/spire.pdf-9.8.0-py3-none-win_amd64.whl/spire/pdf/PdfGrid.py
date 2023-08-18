from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGrid (  PdfLayoutWidget) :
    """

    """
    @property

    def Headers(self)->'PdfGridHeaderCollection':
        """
    <summary>
        Gets the headers.
    </summary>
<value>The headers.</value>
        """
        GetDllLibPdf().PdfGrid_get_Headers.argtypes=[c_void_p]
        GetDllLibPdf().PdfGrid_get_Headers.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_get_Headers(self.Ptr)
        ret = None if intPtr==None else PdfGridHeaderCollection(intPtr)
        return ret


    @property

    def Rows(self)->'PdfGridRowCollection':
        """
    <summary>
        Gets the rows.
    </summary>
<value>The rows.</value>
        """
        GetDllLibPdf().PdfGrid_get_Rows.argtypes=[c_void_p]
        GetDllLibPdf().PdfGrid_get_Rows.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_get_Rows(self.Ptr)
        ret = None if intPtr==None else PdfGridRowCollection(intPtr)
        return ret


    @property

    def DataSource(self)->'SpireObject':
        """
    <summary>
        Gets or sets the data source.
    </summary>
<value>The data source.</value>
        """
        GetDllLibPdf().PdfGrid_get_DataSource.argtypes=[c_void_p]
        GetDllLibPdf().PdfGrid_get_DataSource.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_get_DataSource(self.Ptr)
        ret = None if intPtr==None else SpireObject(intPtr)
        return ret


    @DataSource.setter
    def DataSource(self, value:'SpireObject'):
        GetDllLibPdf().PdfGrid_set_DataSource.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGrid_set_DataSource(self.Ptr, value.Ptr)

    @property

    def DataMember(self)->str:
        """
    <summary>
        Gets or sets the data member.
    </summary>
<value>The data member.</value>
        """
        GetDllLibPdf().PdfGrid_get_DataMember.argtypes=[c_void_p]
        GetDllLibPdf().PdfGrid_get_DataMember.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfGrid_get_DataMember(self.Ptr))
        return ret


    @DataMember.setter
    def DataMember(self, value:str):
        GetDllLibPdf().PdfGrid_set_DataMember.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfGrid_set_DataMember(self.Ptr, value)

    @property

    def Style(self)->'PdfGridStyle':
        """
    <summary>
        Gets or sets the style.
    </summary>
<value>The style.</value>
        """
        GetDllLibPdf().PdfGrid_get_Style.argtypes=[c_void_p]
        GetDllLibPdf().PdfGrid_get_Style.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_get_Style(self.Ptr)
        ret = None if intPtr==None else PdfGridStyle(intPtr)
        return ret


    @Style.setter
    def Style(self, value:'PdfGridStyle'):
        GetDllLibPdf().PdfGrid_set_Style.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfGrid_set_Style(self.Ptr, value.Ptr)

    @property

    def Columns(self)->'PdfGridColumnCollection':
        """
    <summary>
        Gets the columns.
    </summary>
<value>The columns.</value>
        """
        GetDllLibPdf().PdfGrid_get_Columns.argtypes=[c_void_p]
        GetDllLibPdf().PdfGrid_get_Columns.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_get_Columns(self.Ptr)
        ret = None if intPtr==None else PdfGridColumnCollection(intPtr)
        return ret


    @property
    def RepeatHeader(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether [repeat header].
    </summary>
<value>
  <c>true</c> if [repeat header]; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfGrid_get_RepeatHeader.argtypes=[c_void_p]
        GetDllLibPdf().PdfGrid_get_RepeatHeader.restype=c_bool
        ret = GetDllLibPdf().PdfGrid_get_RepeatHeader(self.Ptr)
        return ret

    @RepeatHeader.setter
    def RepeatHeader(self, value:bool):
        GetDllLibPdf().PdfGrid_set_RepeatHeader.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfGrid_set_RepeatHeader(self.Ptr, value)

    @property
    def AllowCrossPages(self)->bool:
        """
    <summary>
        Gets or sets whether to cross a page.
    </summary>
        """
        GetDllLibPdf().PdfGrid_get_AllowCrossPages.argtypes=[c_void_p]
        GetDllLibPdf().PdfGrid_get_AllowCrossPages.restype=c_bool
        ret = GetDllLibPdf().PdfGrid_get_AllowCrossPages(self.Ptr)
        return ret

    @AllowCrossPages.setter
    def AllowCrossPages(self, value:bool):
        GetDllLibPdf().PdfGrid_set_AllowCrossPages.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfGrid_set_AllowCrossPages(self.Ptr, value)

    @dispatch

    def Draw(self ,graphics:'PdfCanvas',location:PointF,width:float):
        """
    <summary>
        Draws the specified graphics.
    </summary>
    <param name="graphics">The graphics.</param>
    <param name="location">The location.</param>
    <param name="width">The width.</param>
        """
        intPtrgraphics:c_void_p = graphics.Ptr
        intPtrlocation:c_void_p = location.Ptr

        GetDllLibPdf().PdfGrid_Draw.argtypes=[c_void_p ,c_void_p,c_void_p,c_float]
        GetDllLibPdf().PdfGrid_Draw(self.Ptr, intPtrgraphics,intPtrlocation,width)

    @dispatch

    def Draw(self ,graphics:PdfCanvas,x:float,y:float,width:float):
        """
    <summary>
        Draws the specified graphics.
    </summary>
    <param name="graphics">The graphics.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
        """
        intPtrgraphics:c_void_p = graphics.Ptr

        GetDllLibPdf().PdfGrid_DrawGXYW.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float]
        GetDllLibPdf().PdfGrid_DrawGXYW(self.Ptr, intPtrgraphics,x,y,width)

    @dispatch

    def Draw(self ,graphics:PdfCanvas,bounds:RectangleF):
        """
    <summary>
        Draws the specified graphics.
    </summary>
    <param name="graphics">The graphics.</param>
    <param name="bounds">The bounds.</param>
        """
        intPtrgraphics:c_void_p = graphics.Ptr
        intPtrbounds:c_void_p = bounds.Ptr

        GetDllLibPdf().PdfGrid_DrawGB.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfGrid_DrawGB(self.Ptr, intPtrgraphics,intPtrbounds)

    @dispatch

    def Draw(self ,page:'PdfNewPage',location:PointF)->PdfGridLayoutResult:
        """
    <summary>
        Draws the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="location">The location.</param>
    <returns></returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlocation:c_void_p = location.Ptr

        GetDllLibPdf().PdfGrid_DrawPL.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfGrid_DrawPL.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_DrawPL(self.Ptr, intPtrpage,intPtrlocation)
        ret = None if intPtr==None else PdfGridLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',location:PointF,format:PdfGridLayoutFormat)->PdfGridLayoutResult:
        """
    <summary>
        Draws the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="location">The location.</param>
    <param name="format">The format.</param>
    <returns></returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlocation:c_void_p = location.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfGrid_DrawPLF.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfGrid_DrawPLF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_DrawPLF(self.Ptr, intPtrpage,intPtrlocation,intPtrformat)
        ret = None if intPtr==None else PdfGridLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',bounds:RectangleF)->PdfGridLayoutResult:
        """
    <summary>
        Draws the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="bounds">The bounds.</param>
    <returns></returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrbounds:c_void_p = bounds.Ptr

        GetDllLibPdf().PdfGrid_DrawPB.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfGrid_DrawPB.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_DrawPB(self.Ptr, intPtrpage,intPtrbounds)
        ret = None if intPtr==None else PdfGridLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',bounds:RectangleF,format:PdfGridLayoutFormat)->PdfGridLayoutResult:
        """
    <summary>
        Draws the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="bounds">The bounds.</param>
    <param name="format">The format.</param>
    <returns></returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrbounds:c_void_p = bounds.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfGrid_DrawPBF.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfGrid_DrawPBF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_DrawPBF(self.Ptr, intPtrpage,intPtrbounds,intPtrformat)
        ret = None if intPtr==None else PdfGridLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',x:float,y:float)->PdfGridLayoutResult:
        """
    <summary>
        Draws the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <returns></returns>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfGrid_DrawPXY.argtypes=[c_void_p ,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfGrid_DrawPXY.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_DrawPXY(self.Ptr, intPtrpage,x,y)
        ret = None if intPtr==None else PdfGridLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',x:float,y:float,format:PdfGridLayoutFormat)->PdfGridLayoutResult:
        """
    <summary>
        Draws the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="format">The format.</param>
    <returns></returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfGrid_DrawPXYF.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_void_p]
        GetDllLibPdf().PdfGrid_DrawPXYF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_DrawPXYF(self.Ptr, intPtrpage,x,y,intPtrformat)
        ret = None if intPtr==None else PdfGridLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',x:float,y:float,width:float)->PdfGridLayoutResult:
        """
    <summary>
        Draws the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <returns></returns>
        """
        intPtrpage:c_void_p = page.Ptr

        GetDllLibPdf().PdfGrid_DrawPXYW.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float]
        GetDllLibPdf().PdfGrid_DrawPXYW.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_DrawPXYW(self.Ptr, intPtrpage,x,y,width)
        ret = None if intPtr==None else PdfGridLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,page:'PdfNewPage',x:float,y:float,width:float,format:PdfGridLayoutFormat)->PdfGridLayoutResult:
        """
    <summary>
        Draws the specified page.
    </summary>
    <param name="page">The page.</param>
    <param name="x">The x.</param>
    <param name="y">The y.</param>
    <param name="width">The width.</param>
    <param name="format">The format.</param>
    <returns></returns>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfGrid_DrawPXYWF.argtypes=[c_void_p ,c_void_p,c_float,c_float,c_float,c_void_p]
        GetDllLibPdf().PdfGrid_DrawPXYWF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfGrid_DrawPXYWF(self.Ptr, intPtrpage,x,y,width,intPtrformat)
        ret = None if intPtr==None else PdfGridLayoutResult(intPtr)
        return ret


