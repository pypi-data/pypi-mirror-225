from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfGraphicsWidget (SpireObject) :
    """
    <summary>
        Represents a base class for all page graphics elements.
    </summary>
    """
    @dispatch

    def Draw(self ,graphics:PdfCanvas):
        """
    <summary>
        Draws an element on the Graphics.
    </summary>
    <param name="graphics">Graphics context where the element should be printed.</param>
        """
        intPtrgraphics:c_void_p = graphics.Ptr

        GetDllLibPdf().PdfGraphicsWidget_Draw.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfGraphicsWidget_Draw(self.Ptr, intPtrgraphics)

    @dispatch

    def Draw(self ,graphics:PdfCanvas,location:PointF):
        """
    <summary>
        Draws an element on the Graphics.
    </summary>
    <param name="graphics">Graphics context where the element should be printed.</param>
    <param name="location">Location of the element in the Graphics' co-ordinate system.</param>
        """
        intPtrgraphics:c_void_p = graphics.Ptr
        intPtrlocation:c_void_p = location.Ptr

        GetDllLibPdf().PdfGraphicsWidget_DrawGL.argtypes=[c_void_p ,c_void_p,c_void_p]
        GetDllLibPdf().PdfGraphicsWidget_DrawGL(self.Ptr, intPtrgraphics,intPtrlocation)

    @dispatch

    def Draw(self ,graphics:PdfCanvas,x:float,y:float):
        """
    <summary>
        Draws an element on the Graphics.
    </summary>
    <param name="graphics">Graphics context where the element should be printed.</param>
    <param name="x">X co-ordinate of the element.</param>
    <param name="y">Y co-ordinate of the element.</param>
        """
        intPtrgraphics:c_void_p = graphics.Ptr

        GetDllLibPdf().PdfGraphicsWidget_DrawGXY.argtypes=[c_void_p ,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfGraphicsWidget_DrawGXY(self.Ptr, intPtrgraphics,x,y)

