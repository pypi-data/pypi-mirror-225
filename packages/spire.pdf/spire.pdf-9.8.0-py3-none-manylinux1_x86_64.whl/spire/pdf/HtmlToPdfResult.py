from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class HtmlToPdfResult (SpireObject) :
    """
    <summary>
        Represents the result of html to pdf conversion.
    </summary>
    """
    @property

    def RenderedImage(self)->'Image':
        """
    <summary>
        Gets the rendered image.
    </summary>
<value>The rendered image.</value>
        """
        GetDllLibPdf().HtmlToPdfResult_get_RenderedImage.argtypes=[c_void_p]
        GetDllLibPdf().HtmlToPdfResult_get_RenderedImage.restype=c_void_p
        intPtr = GetDllLibPdf().HtmlToPdfResult_get_RenderedImage(self.Ptr)
        ret = None if intPtr==None else Image(intPtr)
        return ret



    def Render(self ,page:'PdfPageBase',format:'PdfTextLayout')->'PdfLayoutResult':
        """
    <summary>
        Draws the HtmlToPdfResults on to the document.
    </summary>
    <param name="page">The Pdf Page.</param>
    <param name="format">The Metafile layout format.</param>
        """
        intPtrpage:c_void_p = page.Ptr
        intPtrformat:c_void_p = format.Ptr

        GetDllLibPdf().HtmlToPdfResult_Render.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().HtmlToPdfResult_Render.restype=c_void_p
        intPtr = GetDllLibPdf().HtmlToPdfResult_Render(self.Ptr, intPtrpage,intPtrformat)
        ret = None if intPtr==None else PdfLayoutResult(intPtr)
        return ret


