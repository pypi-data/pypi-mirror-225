from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfListBase (  PdfLayoutWidget) :
    """
    <summary>
        Represents base class for lists.
    </summary>
    """
    @property

    def Items(self)->'PdfListItemCollection':
        """
    <summary>
        Gets items of the list.
    </summary>
        """
        GetDllLibPdf().PdfListBase_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().PdfListBase_get_Items.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListBase_get_Items(self.Ptr)
        ret = None if intPtr==None else PdfListItemCollection(intPtr)
        return ret


    @property
    def Indent(self)->float:
        """
    <summary>
        Gets or sets tabulation for the list.
    </summary>
        """
        GetDllLibPdf().PdfListBase_get_Indent.argtypes=[c_void_p]
        GetDllLibPdf().PdfListBase_get_Indent.restype=c_float
        ret = GetDllLibPdf().PdfListBase_get_Indent(self.Ptr)
        return ret

    @Indent.setter
    def Indent(self, value:float):
        GetDllLibPdf().PdfListBase_set_Indent.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfListBase_set_Indent(self.Ptr, value)

    @property
    def TextIndent(self)->float:
        """
    <summary>
        Gets or sets the indent from the marker to the list item text.
    </summary>
        """
        GetDllLibPdf().PdfListBase_get_TextIndent.argtypes=[c_void_p]
        GetDllLibPdf().PdfListBase_get_TextIndent.restype=c_float
        ret = GetDllLibPdf().PdfListBase_get_TextIndent(self.Ptr)
        return ret

    @TextIndent.setter
    def TextIndent(self, value:float):
        GetDllLibPdf().PdfListBase_set_TextIndent.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfListBase_set_TextIndent(self.Ptr, value)

    @property

    def Font(self)->'PdfFontBase':
        """
    <summary>
        Gets or sets the list font.
    </summary>
        """
        GetDllLibPdf().PdfListBase_get_Font.argtypes=[c_void_p]
        GetDllLibPdf().PdfListBase_get_Font.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListBase_get_Font(self.Ptr)
        ret = None if intPtr==None else PdfFontBase(intPtr)
        return ret


    @Font.setter
    def Font(self, value:'PdfFontBase'):
        GetDllLibPdf().PdfListBase_set_Font.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfListBase_set_Font(self.Ptr, value.Ptr)

    @property

    def Brush(self)->'PdfBrush':
        """
    <summary>
        Gets or sets list brush.
    </summary>
        """
        GetDllLibPdf().PdfListBase_get_Brush.argtypes=[c_void_p]
        GetDllLibPdf().PdfListBase_get_Brush.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListBase_get_Brush(self.Ptr)
        ret = None if intPtr==None else PdfBrush(intPtr)
        return ret


    @Brush.setter
    def Brush(self, value:'PdfBrush'):
        GetDllLibPdf().PdfListBase_set_Brush.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfListBase_set_Brush(self.Ptr, value.Ptr)

    @property

    def Pen(self)->'PdfPen':
        """
    <summary>
        Gets or sets list pen.
    </summary>
        """
        GetDllLibPdf().PdfListBase_get_Pen.argtypes=[c_void_p]
        GetDllLibPdf().PdfListBase_get_Pen.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListBase_get_Pen(self.Ptr)
        ret = None if intPtr==None else PdfPen(intPtr)
        return ret


    @Pen.setter
    def Pen(self, value:'PdfPen'):
        GetDllLibPdf().PdfListBase_set_Pen.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfListBase_set_Pen(self.Ptr, value.Ptr)

    @property

    def StringFormat(self)->'PdfStringFormat':
        """
    <summary>
        Gets or sets the format of the list.
    </summary>
<value>The format.</value>
        """
        GetDllLibPdf().PdfListBase_get_StringFormat.argtypes=[c_void_p]
        GetDllLibPdf().PdfListBase_get_StringFormat.restype=c_void_p
        intPtr = GetDllLibPdf().PdfListBase_get_StringFormat(self.Ptr)
        ret = None if intPtr==None else PdfStringFormat(intPtr)
        return ret


    @StringFormat.setter
    def StringFormat(self, value:'PdfStringFormat'):
        GetDllLibPdf().PdfListBase_set_StringFormat.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfListBase_set_StringFormat(self.Ptr, value.Ptr)


    def add_BeginItemLayout(self ,value:'BeginItemLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfListBase_add_BeginItemLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListBase_add_BeginItemLayout(self.Ptr, intPtrvalue)


    def remove_BeginItemLayout(self ,value:'BeginItemLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfListBase_remove_BeginItemLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListBase_remove_BeginItemLayout(self.Ptr, intPtrvalue)


    def add_EndItemLayout(self ,value:'EndItemLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfListBase_add_EndItemLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListBase_add_EndItemLayout(self.Ptr, intPtrvalue)


    def remove_EndItemLayout(self ,value:'EndItemLayoutEventHandler'):
        """

        """
        intPtrvalue:c_void_p = value.Ptr

        GetDllLibPdf().PdfListBase_remove_EndItemLayout.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfListBase_remove_EndItemLayout(self.Ptr, intPtrvalue)


    def Draw(self ,graphics:'PdfCanvas',x:float,y:float):
        """
    <summary>
        Draws an list on the Graphics.
    </summary>
    <param name="graphics">Graphics context where the list should be printed.</param>
    <param name="x">X co-ordinate of the list.</param>
    <param name="y">Y co-ordinate of the list.</param>
        """
        intPtrgraphics:c_void_p = graphics.Ptr

        GetDllLibPdf().PdfListBase_Draw.argtypes=[c_void_p ,c_void_p,c_float,c_float]
        GetDllLibPdf().PdfListBase_Draw(self.Ptr, intPtrgraphics,x,y)

