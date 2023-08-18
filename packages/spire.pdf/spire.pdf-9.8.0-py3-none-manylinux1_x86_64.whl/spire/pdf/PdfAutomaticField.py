from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAutomaticField (  PdfGraphicsWidget) :
    """
    <summary>
        Represents a fields which is calculated before the document saves.
    </summary>
    """
    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets or sets the bounds of the field.
    </summary>
<value>The bounds value.</value>
        """
        GetDllLibPdf().PdfAutomaticField_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfAutomaticField_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAutomaticField_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Bounds.setter
    def Bounds(self, value:'RectangleF'):
        GetDllLibPdf().PdfAutomaticField_set_Bounds.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAutomaticField_set_Bounds(self.Ptr, value.Ptr)

    @property

    def Size(self)->'SizeF':
        """
    <summary>
        Gets or sets the size of the field.
    </summary>
<value>The size of the field.</value>
        """
        GetDllLibPdf().PdfAutomaticField_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfAutomaticField_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAutomaticField_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @Size.setter
    def Size(self, value:'SizeF'):
        GetDllLibPdf().PdfAutomaticField_set_Size.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAutomaticField_set_Size(self.Ptr, value.Ptr)

    @property

    def Location(self)->'PointF':
        """
    <summary>
        Gets or sets the location of the field.
    </summary>
<value>The location.</value>
        """
        GetDllLibPdf().PdfAutomaticField_get_Location.argtypes=[c_void_p]
        GetDllLibPdf().PdfAutomaticField_get_Location.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAutomaticField_get_Location(self.Ptr)
        ret = None if intPtr==None else PointF(intPtr)
        return ret


    @Location.setter
    def Location(self, value:'PointF'):
        GetDllLibPdf().PdfAutomaticField_set_Location.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAutomaticField_set_Location(self.Ptr, value.Ptr)

    @property

    def Font(self)->'PdfFontBase':
        """
    <summary>
        Gets or sets the font.
    </summary>
<value>The font.</value>
        """
        GetDllLibPdf().PdfAutomaticField_get_Font.argtypes=[c_void_p]
        GetDllLibPdf().PdfAutomaticField_get_Font.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAutomaticField_get_Font(self.Ptr)
        ret = None if intPtr==None else PdfFontBase(intPtr)
        return ret


    @Font.setter
    def Font(self, value:'PdfFontBase'):
        GetDllLibPdf().PdfAutomaticField_set_Font.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAutomaticField_set_Font(self.Ptr, value.Ptr)

    @property

    def Brush(self)->'PdfBrush':
        """
    <summary>
        Gets or sets the brush.
    </summary>
<value>The brush.</value>
        """
        GetDllLibPdf().PdfAutomaticField_get_Brush.argtypes=[c_void_p]
        GetDllLibPdf().PdfAutomaticField_get_Brush.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAutomaticField_get_Brush(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @Brush.setter
    def Brush(self, value:'PdfBrush'):
        GetDllLibPdf().PdfAutomaticField_set_Brush.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAutomaticField_set_Brush(self.Ptr, value.Ptr)

    @property

    def Pen(self)->'PdfPen':
        """
    <summary>
        Gets or sets the pen.
    </summary>
<value>The pen.</value>
        """
        GetDllLibPdf().PdfAutomaticField_get_Pen.argtypes=[c_void_p]
        GetDllLibPdf().PdfAutomaticField_get_Pen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAutomaticField_get_Pen(self.Ptr)
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @Pen.setter
    def Pen(self, value:'PdfPen'):
        GetDllLibPdf().PdfAutomaticField_set_Pen.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAutomaticField_set_Pen(self.Ptr, value.Ptr)

    @property

    def StringFormat(self)->'PdfStringFormat':
        """
    <summary>
        Gets or sets the string format.
    </summary>
<value>The string format.</value>
        """
        GetDllLibPdf().PdfAutomaticField_get_StringFormat.argtypes=[c_void_p]
        GetDllLibPdf().PdfAutomaticField_get_StringFormat.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAutomaticField_get_StringFormat(self.Ptr)
        ret = None if intPtr==None else PdfStringFormat(intPtr)
        return ret


    @StringFormat.setter
    def StringFormat(self, value:'PdfStringFormat'):
        GetDllLibPdf().PdfAutomaticField_set_StringFormat.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAutomaticField_set_StringFormat(self.Ptr, value.Ptr)


    def Draw(self ,graphics:'PdfCanvas',x:float,y:float):
        """
    <summary>
        Draws an element on the Graphics.
    </summary>
    <param name="graphics">Graphics context where the element should be printed.</param>
    <param name="x">X co-ordinate of the element.</param>
    <param name="y">Y co-ordinate of the element.</param>
<exclude />
        """
        intPtrgraphics:c_void_p = graphics.Ptr

        GetDllLibPdf().PdfAutomaticField_Draw.argtypes=[c_void_p ,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfAutomaticField_Draw(self.Ptr, intPtrgraphics,x,y)

