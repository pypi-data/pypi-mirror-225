from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class IPdfTextBoxField (abc.ABC) :
    """

    """
    @property

    @abc.abstractmethod
    def BackColor(self)->'PdfRGBColor':
        """
    <summary>
        Get or Set the background color of the field
    </summary>
<value>A  object specifying the background color of field. </value>
        """
        pass


    @BackColor.setter
    @abc.abstractmethod
    def BackColor(self, value:'PdfRGBColor'):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def ForeColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or Set the fore color of the field.
    </summary>
<value>A  object specifying the background color of field.</value>
        """
        pass


    @ForeColor.setter
    @abc.abstractmethod
    def ForeColor(self, value:'PdfRGBColor'):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def TextAlignment(self)->'PdfTextAlignment':
        """
    <summary>
        Get or Set the text alignment in a text box.
    </summary>
<value>A  enumeration member specifying the text alignment in a text box.</value>
        """
        pass


    @TextAlignment.setter
    @abc.abstractmethod
    def TextAlignment(self, value:'PdfTextAlignment'):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def HighlightMode(self)->'PdfHighlightMode':
        """
    <summary>
        Get or Set the HighLightMode of the Field.
    </summary>
<value>A  enumeration member specifying the highlight mode in a text box.</value>
        """
        pass


    @HighlightMode.setter
    @abc.abstractmethod
    def HighlightMode(self, value:'PdfHighlightMode'):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def Text(self)->str:
        """
    <summary>
        Gets or Set value of the text box field.
    </summary>
<value>A string value representing the value of the item. </value>
        """
        pass


    @Text.setter
    @abc.abstractmethod
    def Text(self, value:str):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def DefaultValue(self)->str:
        """
    <summary>
        Gets or set the default value of the field.
    </summary>
<value>A string value representing the default value of the item. </value>
        """
        pass


    @DefaultValue.setter
    @abc.abstractmethod
    def DefaultValue(self, value:str):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def SpellCheck(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to check spelling.
    </summary>
<value>True if the field content should be checked for spelling erorrs, false otherwise. Default is true.</value>
        """
        pass


    @SpellCheck.setter
    @abc.abstractmethod
    def SpellCheck(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def InsertSpaces(self)->bool:
        """
    <summary>
        Meaningful only if the MaxLength property is set and the Multiline, Password properties are false.
            If set, the field is automatically divided into as many equally spaced positions, or combs, 
            as the value of MaxLength, and the text is laid out into those combs.
    </summary>
        """
        pass


    @InsertSpaces.setter
    @abc.abstractmethod
    def InsertSpaces(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def Multiline(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is multiline.
    </summary>
<value>True if the field is multiline, false otherwise. Default is false.</value>
        """
        pass


    @Multiline.setter
    @abc.abstractmethod
    def Multiline(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def Password(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is password field.
    </summary>
<value>True if the field is a password field, false otherwise. Default is false.</value>
        """
        pass


    @Password.setter
    @abc.abstractmethod
    def Password(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def Scrollable(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is scrollable.
    </summary>
<value>True if the field content can be scrolled, false otherwise. Default is true.</value>
        """
        pass


    @Scrollable.setter
    @abc.abstractmethod
    def Scrollable(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def MaxLength(self)->int:
        """
    <summary>
        Gets or sets the maximum length of the field, in characters.
    </summary>
<value>A positive integer value specifying the maximum number of characters that can be entered in the text edit field.</value>
        """
        pass


    @MaxLength.setter
    @abc.abstractmethod
    def MaxLength(self, value:int):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def Actions(self)->'PdfFieldActions':
        """
    <summary>
        Gets the actions of the field.
    </summary>
<value>The actions.</value>
        """
        pass


    @property

    @abc.abstractmethod
    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets or sets the bounds.
    </summary>
        """
        pass


    @Bounds.setter
    @abc.abstractmethod
    def Bounds(self, value:'RectangleF'):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def Location(self)->'PointF':
        """
    <summary>
        Gets or sets the location.
    </summary>
        """
        pass


    @Location.setter
    @abc.abstractmethod
    def Location(self, value:'PointF'):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def Size(self)->'SizeF':
        """
    <summary>
        Gets or sets the size.
    </summary>
        """
        pass


    @Size.setter
    @abc.abstractmethod
    def Size(self, value:'SizeF'):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def BorderStyle(self)->'PdfBorderStyle':
        """
    <summary>
        Gets or sets the color of the border.
    </summary>
<value>The color of the border.</value>
        """
        pass


    @BorderStyle.setter
    @abc.abstractmethod
    def BorderStyle(self, value:'PdfBorderStyle'):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def BorderColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the color of the border.
    </summary>
<value>The color of the border.</value>
        """
        pass


    @BorderColor.setter
    @abc.abstractmethod
    def BorderColor(self, value:'PdfRGBColor'):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def BorderWidth(self)->float:
        """
    <summary>
        Gets or Sets the width of the border.
    </summary>
<value>The width of the border.</value>
        """
        pass


    @BorderWidth.setter
    @abc.abstractmethod
    def BorderWidth(self, value:float):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def Font(self)->'PdfFontBase':
        """
    <summary>
        Gets the font.
    </summary>
<value>The font.</value>
        """
        pass


    @Font.setter
    @abc.abstractmethod
    def Font(self, value:'PdfFontBase'):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def Visible(self)->bool:
        """
    <summary>
        Gets a value indicating the visibility of the field.
    </summary>
        """
        pass


    @property

    @abc.abstractmethod
    def Name(self)->str:
        """
    <summary>
        Gets the name of the field.
    </summary>
<value>A string value specifying the name of the field.</value>
        """
        pass


    @property

    @abc.abstractmethod
    def MappingName(self)->str:
        """
    <summary>
        Gets or sets the mapping name to be used when exporting interactive form
            field data from the document.
    </summary>
<value>A string value specifying the mapping name of the field. </value>
        """
        pass


    @MappingName.setter
    @abc.abstractmethod
    def MappingName(self, value:str):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def ToolTip(self)->str:
        """
    <summary>
        Gets or sets the tool tip.
    </summary>
        """
        pass


    @ToolTip.setter
    @abc.abstractmethod
    def ToolTip(self, value:str):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def Page(self)->'PdfPageBase':
        """
    <summary>
        Gets the page.
    </summary>
        """
        pass


    @property
    @abc.abstractmethod
    def ReadOnly(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether [read only].
    </summary>
<value>True if the field is read-only, false otherwise. Default is false.</value>
        """
        pass


    @ReadOnly.setter
    @abc.abstractmethod
    def ReadOnly(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def Required(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is required.
    </summary>
<value>True if the field is required, false otherwise. Default is false.</value>
        """
        pass


    @Required.setter
    @abc.abstractmethod
    def Required(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def Export(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is export.
    </summary>
<value>
  <c>true</c> if export; otherwise, <c>false</c>.</value>
        """
        pass


    @Export.setter
    @abc.abstractmethod
    def Export(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def Flatten(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is flatten.
    </summary>
        """
        pass


    @Flatten.setter
    @abc.abstractmethod
    def Flatten(self, value:bool):
        """

        """
        pass


