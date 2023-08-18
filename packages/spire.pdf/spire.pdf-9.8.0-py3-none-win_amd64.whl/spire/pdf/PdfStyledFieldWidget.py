from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfStyledFieldWidget (  PdfFieldWidget) :
    """
    <summary>
        Represents loaded styled field.
    </summary>
    """
    @property

    def Actions(self)->'PdfFieldActions':
        """
    <summary>
        Gets the actions of the field.
    </summary>
<value>The actions.</value>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_Actions.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_Actions.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_Actions(self.Ptr)
        ret = None if intPtr==None else PdfFieldActions(intPtr)
        return ret


    @property

    def MouseEnter(self)->'PdfAction':
        """

        """
        GetDllLibPdf().PdfStyledFieldWidget_get_MouseEnter.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_MouseEnter.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_MouseEnter(self.Ptr)
        ret = None if intPtr==None else PdfAction(intPtr)
        return ret


    @MouseEnter.setter
    def MouseEnter(self, value:'PdfAction'):
        GetDllLibPdf().PdfStyledFieldWidget_set_MouseEnter.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_MouseEnter(self.Ptr, value.Ptr)

    @property

    def MouseUp(self)->'PdfAction':
        """
    <summary>
        Gets or sets the action to be performed when the mouse button is released 
            inside the annotations active area..
    </summary>
<value>The mouse up action.</value>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_MouseUp.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_MouseUp.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_MouseUp(self.Ptr)
        ret = None if intPtr==None else PdfAction(intPtr)
        return ret


    @MouseUp.setter
    def MouseUp(self, value:'PdfAction'):
        GetDllLibPdf().PdfStyledFieldWidget_set_MouseUp.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_MouseUp(self.Ptr, value.Ptr)

    @property

    def MouseDown(self)->'PdfAction':
        """
    <summary>
        Gets or sets the action to be performed when the mouse button is pressed inside the 
            annotations active area.
    </summary>
<value>The mouse down action.</value>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_MouseDown.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_MouseDown.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_MouseDown(self.Ptr)
        ret = None if intPtr==None else PdfAction(intPtr)
        return ret


    @MouseDown.setter
    def MouseDown(self, value:'PdfAction'):
        GetDllLibPdf().PdfStyledFieldWidget_set_MouseDown.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_MouseDown(self.Ptr, value.Ptr)

    @property

    def MouseLeave(self)->'PdfAction':
        """

        """
        GetDllLibPdf().PdfStyledFieldWidget_get_MouseLeave.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_MouseLeave.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_MouseLeave(self.Ptr)
        ret = None if intPtr==None else PdfAction(intPtr)
        return ret


    @MouseLeave.setter
    def MouseLeave(self, value:'PdfAction'):
        GetDllLibPdf().PdfStyledFieldWidget_set_MouseLeave.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_MouseLeave(self.Ptr, value.Ptr)

    @property

    def GotFocus(self)->'PdfAction':
        """
    <summary>
        Gets or sets the action to be performed when the annotation receives the 
            input focus.
    </summary>
<value>The got focus action.</value>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_GotFocus.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_GotFocus.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_GotFocus(self.Ptr)
        ret = None if intPtr==None else PdfAction(intPtr)
        return ret


    @GotFocus.setter
    def GotFocus(self, value:'PdfAction'):
        GetDllLibPdf().PdfStyledFieldWidget_set_GotFocus.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_GotFocus(self.Ptr, value.Ptr)

    @property

    def ForeColor(self)->'PdfRGBColor':
        """

        """
        GetDllLibPdf().PdfStyledFieldWidget_get_ForeColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_ForeColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_ForeColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @ForeColor.setter
    def ForeColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfStyledFieldWidget_set_ForeColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_ForeColor(self.Ptr, value.Ptr)

    @property

    def BackColor(self)->'PdfRGBColor':
        """
    <summary>
        Get or Set the background color of the field
    </summary>
<value>A  object specifying the background color of field. </value>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_BackColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_BackColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_BackColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @BackColor.setter
    def BackColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfStyledFieldWidget_set_BackColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_BackColor(self.Ptr, value.Ptr)

    @property

    def LostFocus(self)->'PdfAction':
        """
    <summary>
        Gets or sets the action to be performed when the annotation loses the 
            input focus.
    </summary>
<value>The lost focus action.</value>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_LostFocus.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_LostFocus.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_LostFocus(self.Ptr)
        ret = None if intPtr==None else PdfAction(intPtr)
        return ret


    @LostFocus.setter
    def LostFocus(self, value:'PdfAction'):
        GetDllLibPdf().PdfStyledFieldWidget_set_LostFocus.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_LostFocus(self.Ptr, value.Ptr)

    @property

    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets or sets the bounds.
    </summary>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_Bounds.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_Bounds.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_Bounds(self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @Bounds.setter
    def Bounds(self, value:'RectangleF'):
        GetDllLibPdf().PdfStyledFieldWidget_set_Bounds.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_Bounds(self.Ptr, value.Ptr)

    @property

    def Location(self)->'PointF':
        """
    <summary>
        Gets or sets the location.
    </summary>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_Location.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_Location.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_Location(self.Ptr)
        ret = None if intPtr==None else PointF(intPtr)
        return ret


    @Location.setter
    def Location(self, value:'PointF'):
        GetDllLibPdf().PdfStyledFieldWidget_set_Location.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_Location(self.Ptr, value.Ptr)

    @property

    def Size(self)->'SizeF':
        """
    <summary>
        Gets or sets the size.
    </summary>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_Size.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_Size(self.Ptr)
        ret = None if intPtr==None else SizeF(intPtr)
        return ret


    @Size.setter
    def Size(self, value:'SizeF'):
        GetDllLibPdf().PdfStyledFieldWidget_set_Size.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_Size(self.Ptr, value.Ptr)

    @property

    def BorderStyle(self)->'PdfBorderStyle':
        """
    <summary>
        Gets or sets the color of the border.
    </summary>
<value>The color of the border.</value>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_BorderStyle.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_BorderStyle.restype=c_int
        ret = GetDllLibPdf().PdfStyledFieldWidget_get_BorderStyle(self.Ptr)
        objwraped = PdfBorderStyle(ret)
        return objwraped

    @BorderStyle.setter
    def BorderStyle(self, value:'PdfBorderStyle'):
        GetDllLibPdf().PdfStyledFieldWidget_set_BorderStyle.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfStyledFieldWidget_set_BorderStyle(self.Ptr, value.value)

    @property

    def BorderColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the color of the border.
    </summary>
<value>The color of the border.</value>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_BorderColor.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_BorderColor.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_BorderColor(self.Ptr)
        ret = None if intPtr==None else PdfRGBColor(intPtr)
        return ret


    @BorderColor.setter
    def BorderColor(self, value:'PdfRGBColor'):
        GetDllLibPdf().PdfStyledFieldWidget_set_BorderColor.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_BorderColor(self.Ptr, value.Ptr)

    @property
    def BorderWidth(self)->float:
        """
    <summary>
        Gets or Sets the width of the border.
    </summary>
<value>The width of the border.</value>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_BorderWidth.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_BorderWidth.restype=c_float
        ret = GetDllLibPdf().PdfStyledFieldWidget_get_BorderWidth(self.Ptr)
        return ret

    @BorderWidth.setter
    def BorderWidth(self, value:float):
        GetDllLibPdf().PdfStyledFieldWidget_set_BorderWidth.argtypes=[c_void_p, c_float]
        GetDllLibPdf().PdfStyledFieldWidget_set_BorderWidth(self.Ptr, value)

    @property

    def Font(self)->'PdfFontBase':
        """
    <summary>
        Gets the font.
    </summary>
<value>The font.</value>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_Font.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_Font.restype=c_void_p
        intPtr = GetDllLibPdf().PdfStyledFieldWidget_get_Font(self.Ptr)
        ret = None if intPtr==None else PdfFontBase(intPtr)
        return ret


    @Font.setter
    def Font(self, value:'PdfFontBase'):
        GetDllLibPdf().PdfStyledFieldWidget_set_Font.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_set_Font(self.Ptr, value.Ptr)

    @property
    def DefaultIndex(self)->int:
        """
    <summary>
        Gets the default index.
    </summary>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_DefaultIndex.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_DefaultIndex.restype=c_int
        ret = GetDllLibPdf().PdfStyledFieldWidget_get_DefaultIndex(self.Ptr)
        return ret

    @DefaultIndex.setter
    def DefaultIndex(self, value:int):
        GetDllLibPdf().PdfStyledFieldWidget_set_DefaultIndex.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfStyledFieldWidget_set_DefaultIndex(self.Ptr, value)

    @property
    def Visible(self)->bool:
        """
    <summary>
        Gets a value indicating the visibility of the field.
    </summary>
        """
        GetDllLibPdf().PdfStyledFieldWidget_get_Visible.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_get_Visible.restype=c_bool
        ret = GetDllLibPdf().PdfStyledFieldWidget_get_Visible(self.Ptr)
        return ret

    def ObjectID(self)->int:
        """
    <summary>
        Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfStyledFieldWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfStyledFieldWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfStyledFieldWidget_ObjectID(self.Ptr)
        return ret

