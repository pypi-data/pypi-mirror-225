from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTilingBrush (  PdfBrush) :
    @dispatch
    def __init__(self, rectangle:RectangleF):
        ptrRec:c_void_p = rectangle.Ptr
        GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushR.argtypes=[c_void_p]
        GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushR.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushR(ptrRec)
        super(PdfTilingBrush, self).__init__(intPtr)

    @dispatch
    def __init__(self, rectangle:RectangleF,page):
        ptrRec:c_void_p = rectangle.Ptr
        ptrPage:c_void_p = page.Ptr
        GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushRP.argtypes=[c_void_p,c_void_p]
        GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushRP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushRP(ptrRec,ptrPage)
        super(PdfTilingBrush, self).__init__(intPtr)

    @dispatch
    def __init__(self, size:SizeF):
        ptrSize:c_void_p = size.Ptr
        GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushS.argtypes=[c_void_p]
        GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushS.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushS(ptrSize)
        super(PdfTilingBrush, self).__init__(intPtr)

    @dispatch
    def __init__(self, size:SizeF,page):
        ptrSize:c_void_p = size.Ptr
        ptrPage:c_void_p = page.Ptr
        GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushSP.argtypes=[c_void_p]
        GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushSP.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTilingBrush_CreatePdfTilingBrushSP(ptrSize,ptrPage)
        super(PdfTilingBrush, self).__init__(intPtr)
    """
    <summary>
        Implements a colored tiling brush.
    </summary>
    """
    @property

    def Rectangle(self)->'RectangleF':
        """
    <summary>
        Gets the boundary box of the smallest brush cell.
    </summary>
        """
        GetDllLibPdf().PdfTilingBrush_get_Rectangle.argtypes=[c_void_p]
        GetDllLibPdf().PdfTilingBrush_get_Rectangle.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTilingBrush_get_Rectangle(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @property

    def Size(self)->'SizeF':
        """
    <summary>
        Gets the size of the smallest brush cell.
    </summary>
        """
        GetDllLibPdf().PdfTilingBrush_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfTilingBrush_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTilingBrush_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @property

    def Graphics(self)->'PdfCanvas':
        """
    <summary>
        Gets Graphics context of the brush.
    </summary>
        """
        GetDllLibPdf().PdfTilingBrush_get_Graphics.argtypes=[c_void_p]
        GetDllLibPdf().PdfTilingBrush_get_Graphics.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTilingBrush_get_Graphics(self.Ptr)
        ret = None if intPtr==None else PdfCanvas(intPtr)
        return ret



    def Clone(self)->'PdfBrush':
        """
    <summary>
        Creates a new copy of a brush.
    </summary>
    <returns>A new instance of the Brush class.</returns>
        """
        GetDllLibPdf().PdfTilingBrush_Clone.argtypes=[c_void_p]
        GetDllLibPdf().PdfTilingBrush_Clone.restype=c_void_p
        intPtr = GetDllLibPdf().PdfTilingBrush_Clone(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


