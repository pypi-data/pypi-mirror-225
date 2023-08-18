from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfHTMLTextElement (SpireObject) :
    """
    <summary>
        Class that represent HTML text area with the ability to span several pages.
    </summary>
    """
    @property

    def Font(self)->'PdfFontBase':
        """

        """
        GetDllLibPdf().PdfHTMLTextElement_get_Font.argtypes=[c_void_p]
        GetDllLibPdf().PdfHTMLTextElement_get_Font.restype=c_void_p
        intPtr = GetDllLibPdf().PdfHTMLTextElement_get_Font(self.Ptr)
        ret = None if intPtr==None else PdfFontBase(intPtr)
        return ret


    @Font.setter
    def Font(self, value:'PdfFontBase'):
        GetDllLibPdf().PdfHTMLTextElement_set_Font.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfHTMLTextElement_set_Font(self.Ptr, value.Ptr)

    @property

    def Brush(self)->'PdfBrush':
        """

        """
        GetDllLibPdf().PdfHTMLTextElement_get_Brush.argtypes=[c_void_p]
        GetDllLibPdf().PdfHTMLTextElement_get_Brush.restype=c_void_p
        intPtr = GetDllLibPdf().PdfHTMLTextElement_get_Brush(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @Brush.setter
    def Brush(self, value:'PdfBrush'):
        GetDllLibPdf().PdfHTMLTextElement_set_Brush.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfHTMLTextElement_set_Brush(self.Ptr, value.Ptr)

    @property

    def HTMLText(self)->str:
        """

        """
        GetDllLibPdf().PdfHTMLTextElement_get_HTMLText.argtypes=[c_void_p]
        GetDllLibPdf().PdfHTMLTextElement_get_HTMLText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfHTMLTextElement_get_HTMLText(self.Ptr))
        return ret


    @HTMLText.setter
    def HTMLText(self, value:str):
        GetDllLibPdf().PdfHTMLTextElement_set_HTMLText.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfHTMLTextElement_set_HTMLText(self.Ptr, value)

    @property

    def TextAlign(self)->'TextAlign':
        """

        """
        GetDllLibPdf().PdfHTMLTextElement_get_TextAlign.argtypes=[c_void_p]
        GetDllLibPdf().PdfHTMLTextElement_get_TextAlign.restype=c_int
        ret = GetDllLibPdf().PdfHTMLTextElement_get_TextAlign(self.Ptr)
        objwraped = TextAlign(ret)
        return objwraped

    @TextAlign.setter
    def TextAlign(self, value:'TextAlign'):
        GetDllLibPdf().PdfHTMLTextElement_set_TextAlign.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfHTMLTextElement_set_TextAlign(self.Ptr, value.value)

    @dispatch

    def Draw(self ,page:'PdfNewPage',layoutRectangle:RectangleF,format:PdfMetafileLayoutFormat)->PdfLayoutResult:
        """

        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfHTMLTextElement_Draw.argtypes=[c_void_p ,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfHTMLTextElement_Draw.restype=c_void_p
        intPtr = GetDllLibPdf().PdfHTMLTextElement_Draw(self.Ptr, intPtrpage,intPtrlayoutRectangle,intPtrformat)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,graphics:PdfCanvas,layoutRectangle:RectangleF):
        """

        """
        intPtrgraphics:c_void_p = graphics.Ptr
        intPtrlayoutRectangle:c_void_p = layoutRectangle.Ptr

        GetDllLibPdf().PdfHTMLTextElement_DrawGL.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfHTMLTextElement_DrawGL(self.Ptr, intPtrgraphics,intPtrlayoutRectangle)

    @dispatch

    def Draw(self ,page:'PdfNewPage',location:PointF,width:float,format:PdfMetafileLayoutFormat)->PdfLayoutResult:
        """

        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlocation:c_void_p = location.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfHTMLTextElement_DrawPLWF.argtypes=[c_void_p ,c_void_p,c_void_p,c_float,c_void_p]
        GetDllLibPdf().PdfHTMLTextElement_DrawPLWF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfHTMLTextElement_DrawPLWF(self.Ptr, intPtrpage,intPtrlocation,width,intPtrformat)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


    @dispatch

    def Draw(self ,graphics:PdfCanvas,location:PointF,width:float,height:float):
        """

        """
        intPtrgraphics:c_void_p = graphics.Ptr
        intPtrlocation:c_void_p = location.Ptr

        GetDllLibPdf().PdfHTMLTextElement_DrawGLWH.argtypes=[c_void_p ,c_void_p,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfHTMLTextElement_DrawGLWH(self.Ptr, intPtrgraphics,intPtrlocation,width,height)

    @dispatch

    def Draw(self ,page:'PdfNewPage',location:PointF,width:float,height:float,format:PdfMetafileLayoutFormat)->PdfLayoutResult:
        """

        """
        intPtrpage:c_void_p = page.Ptr
        intPtrlocation:c_void_p = location.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().PdfHTMLTextElement_DrawPLWHF.argtypes=[c_void_p ,c_void_p,c_void_p,c_float,c_float,c_void_p]
        GetDllLibPdf().PdfHTMLTextElement_DrawPLWHF.restype=c_void_p
        intPtr = GetDllLibPdf().PdfHTMLTextElement_DrawPLWHF(self.Ptr, intPtrpage,intPtrlocation,width,height,intPtrformat)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


