from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfStyledField (  PdfField) :
    """
    <summary>
        Represents form's field with style parameters.
    </summary>
    """
    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets or sets the bounds.
    </summary>
<value>The bounds.</value>
        """
        GetDllLibPdf().PdfStyledField_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledField_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Bounds.setter
    def Bounds(self, value:'RectangleF'):
        GetDllLibPdf().PdfStyledField_set_Bounds.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledField_set_Bounds(self.Ptr, value.Ptr)

    @property

    def Location(self)->'PointF':
        """
    <summary>
        Gets or sets the location.
    </summary>
<value>The location.</value>
        """
        GetDllLibPdf().PdfStyledField_get_Location.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_Location.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledField_get_Location(self.Ptr)
        ret = None if intPtr==None else PointF(intPtr)
        return ret


    @Location.setter
    def Location(self, value:'PointF'):
        GetDllLibPdf().PdfStyledField_set_Location.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledField_set_Location(self.Ptr, value.Ptr)

    @property

    def Size(self)->'SizeF':
        """
    <summary>
        Gets or sets the size.
    </summary>
<value>The size.</value>
        """
        GetDllLibPdf().PdfStyledField_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledField_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @Size.setter
    def Size(self, value:'SizeF'):
        GetDllLibPdf().PdfStyledField_set_Size.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledField_set_Size(self.Ptr, value.Ptr)

    @property

    def BorderColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the color of the border.
    </summary>
<value>The color of the border.</value>
        """
        GetDllLibPdf().PdfStyledField_get_BorderColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_BorderColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledField_get_BorderColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @BorderColor.setter
    def BorderColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfStyledField_set_BorderColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledField_set_BorderColor(self.Ptr, value.Ptr)

    @property

    def BackColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the color of the background.
    </summary>
<value>The color of the background.</value>
        """
        GetDllLibPdf().PdfStyledField_get_BackColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_BackColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledField_get_BackColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @BackColor.setter
    def BackColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfStyledField_set_BackColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledField_set_BackColor(self.Ptr, value.Ptr)

    @property

    def ForeColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the color of the text.
    </summary>
<value>The color of the text.</value>
        """
        GetDllLibPdf().PdfStyledField_get_ForeColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_ForeColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledField_get_ForeColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @ForeColor.setter
    def ForeColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfStyledField_set_ForeColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledField_set_ForeColor(self.Ptr, value.Ptr)

    @property
    def BorderWidth(self)->float:
        """
    <summary>
        Gets or sets the width of the border.
    </summary>
<value>The width of the border.</value>
        """
        GetDllLibPdf().PdfStyledField_get_BorderWidth.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_BorderWidth.restype=c_float
        ret = GetDllLibPdf().PdfStyledField_get_BorderWidth(self.Ptr)
        return ret

    @BorderWidth.setter
    def BorderWidth(self, value:float):
        GetDllLibPdf().PdfStyledField_set_BorderWidth.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfStyledField_set_BorderWidth(self.Ptr, value)

    @property

    def HighlightMode(self)->'PdfHighlightMode':
        """
    <summary>
        Gets or sets the highlighting mode.
    </summary>
<value>The highlighting mode.</value>
        """
        GetDllLibPdf().PdfStyledField_get_HighlightMode.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_HighlightMode.restype=c_int
        ret = GetDllLibPdf().PdfStyledField_get_HighlightMode(self.Ptr)
        objwraped = PdfHighlightMode(ret)
        return objwraped

    @HighlightMode.setter
    def HighlightMode(self, value:'PdfHighlightMode'):
        GetDllLibPdf().PdfStyledField_set_HighlightMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfStyledField_set_HighlightMode(self.Ptr, value.value)

    @property

    def Font(self)->'PdfFontBase':
        """
    <summary>
        Gets or sets the font.
    </summary>
<value>The font.</value>
        """
        GetDllLibPdf().PdfStyledField_get_Font.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_Font.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledField_get_Font(self.Ptr)
        ret = None if intPtr==None else PdfFontBase(intPtr)
        return ret


    @Font.setter
    def Font(self, value:'PdfFontBase'):
        GetDllLibPdf().PdfStyledField_set_Font.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledField_set_Font(self.Ptr, value.Ptr)

    @property

    def TextAlignment(self)->'PdfTextAlignment':
        """
    <summary>
        Gets or sets the text alignment.
    </summary>
<value>The text alignment.</value>
<remarks>This property is meaningful for fields containing variable text only.
            </remarks>
        """
        GetDllLibPdf().PdfStyledField_get_TextAlignment.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_TextAlignment.restype=c_int
        ret = GetDllLibPdf().PdfStyledField_get_TextAlignment(self.Ptr)
        objwraped = PdfTextAlignment(ret)
        return objwraped

    @TextAlignment.setter
    def TextAlignment(self, value:'PdfTextAlignment'):
        GetDllLibPdf().PdfStyledField_set_TextAlignment.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfStyledField_set_TextAlignment(self.Ptr, value.value)

    @property

    def Actions(self)->'PdfFieldActions':
        """
    <summary>
        Gets the actions of the field.
    </summary>
<value>The actions.</value>
        """
        GetDllLibPdf().PdfStyledField_get_Actions.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_Actions.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledField_get_Actions(self.Ptr)
        ret = None if intPtr==None else PdfFieldActions(intPtr)
        return ret


    @property

    def BorderStyle(self)->'PdfBorderStyle':
        """
    <summary>
        Gets or sets the border style.
    </summary>
<value>The border style.</value>
        """
        GetDllLibPdf().PdfStyledField_get_BorderStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_BorderStyle.restype=c_int
        ret = GetDllLibPdf().PdfStyledField_get_BorderStyle(self.Ptr)
        objwraped = PdfBorderStyle(ret)
        return objwraped

    @BorderStyle.setter
    def BorderStyle(self, value:'PdfBorderStyle'):
        GetDllLibPdf().PdfStyledField_set_BorderStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfStyledField_set_BorderStyle(self.Ptr, value.value)

    @property
    def Visible(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is visible.
    </summary>
<value>
  <c>true</c> if visible; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfStyledField_get_Visible.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledField_get_Visible.restype=c_bool
        ret = GetDllLibPdf().PdfStyledField_get_Visible(self.Ptr)
        return ret

    @Visible.setter
    def Visible(self, value:bool):
        GetDllLibPdf().PdfStyledField_set_Visible.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfStyledField_set_Visible(self.Ptr, value)

