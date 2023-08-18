from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfStringLayouter (SpireObject) :
    @dispatch
    def __init__(self):
        GetDllLibPdf().PdfStringLayouter_CreatePdfStringLayouter.restype = c_void_p
        intPtr = GetDllLibPdf().PdfStringLayouter_CreatePdfStringLayouter()
        super(PdfStringLayouter, self).__init__(intPtr)
    """
    <summary>
        Class lay outing the text.
    </summary>
    """

    def Layout(self ,text:str,font:'PdfFontBase',strFormat:'PdfStringFormat',size:'SizeF')->'PdfStringLayoutResult':
        """
    <summary>
        Layouts the text.
    </summary>
    <param name="text">String text.</param>
    <param name="font">Font for the text.</param>
    <param name="format">String format.</param>
    <param name="size">Bounds of the text.</param>
    <returns>Layout result.</returns>
        """
        intPtrfont:c_void_p = font.Ptr
        intPtrformat:c_void_p = strFormat.Ptr
        intPtrsize:c_void_p = size.Ptr

        GetDllLibPdf().PdfStringLayouter_Layout.argtypes=[c_void_p ,c_wchar_p,c_void_p,c_void_p,c_void_p]
        GetDllLibPdf().PdfStringLayouter_Layout.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStringLayouter_Layout(self.Ptr, text,intPtrfont,intPtrformat,intPtrsize)
        ret = None if intPtr==None else PdfStringLayoutResult(intPtr)
        return ret


