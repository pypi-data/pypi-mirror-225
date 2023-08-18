from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class IPdfComboBoxField (abc.ABC) :
    """

    """
    @property
    @abc.abstractmethod
    def Editable(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is editable.
    </summary>
<value>
  <c>true</c> if editable; otherwise, <c>false</c>.</value>
        """
        pass


    @Editable.setter
    @abc.abstractmethod
    def Editable(self, value:bool):
        """

        """
        pass


    @property
    @abc.abstractmethod
    def SelectedIndex(self)->int:
        """
    <summary>
        Gets or sets the first selected item in the list. 
    </summary>
<value>The index of the selected item.</value>
        """
        pass


    @SelectedIndex.setter
    @abc.abstractmethod
    def SelectedIndex(self, value:int):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def SelectedValue(self)->str:
        """
    <summary>
        Gets or sets the value of the first selected item in the list.
    </summary>
<value>The selected value.</value>
        """
        pass


    @SelectedValue.setter
    @abc.abstractmethod
    def SelectedValue(self, value:str):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def SelectedItem(self)->'PdfListFieldItem':
        """
    <summary>
        Gets the first selected item in the list.
    </summary>
<value>The selected item.</value>
        """
        pass


    @property

    @abc.abstractmethod
    def Bounds(self)->'RectangleF':
        """
    <summary>
        Gets or sets the bounds.
    </summary>
<value>The bounds.</value>
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
<value>The location.</value>
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
<value>The size.</value>
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
    def BackColor(self)->'PdfRGBColor':
        """
    <summary>
        Gets or sets the color of the background.
    </summary>
<value>The color of the background.</value>
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
        Gets or sets the color of the text.
    </summary>
<value>The color of the text.</value>
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
    def BorderWidth(self)->float:
        """
    <summary>
        Gets or sets the width of the border.
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
    def HighlightMode(self)->'PdfHighlightMode':
        """
    <summary>
        Gets or sets the highlighting mode.
    </summary>
<value>The highlighting mode.</value>
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
    def Font(self)->'PdfFontBase':
        """
    <summary>
        Gets or sets the font.
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
    def TextAlignment(self)->'PdfTextAlignment':
        """
    <summary>
        Gets or sets the text alignment.
    </summary>
<value>The text alignment.</value>
<remarks>This property is meaningful for fields containing variable text only.
            </remarks>
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
    def BorderStyle(self)->'PdfBorderStyle':
        """
    <summary>
        Gets or sets the border style.
    </summary>
<value>The border style.</value>
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
    def Visible(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is visible.
    </summary>
<value>
  <c>true</c> if visible; otherwise, <c>false</c>.</value>
        """
        pass


    @Visible.setter
    @abc.abstractmethod
    def Visible(self, value:bool):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def Name(self)->str:
        """
    <summary>
        Gets the name.
    </summary>
<value>The name.</value>
        """
        pass


    @property

    @abc.abstractmethod
    def Form(self)->'PdfForm':
        """
    <summary>
        Gets the form.
    </summary>
<value>The form.</value>
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
<value>The mapping name.</value>
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
    def ReadOnly(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether [read only].
    </summary>
<value> if the field is read only, set to <c>true</c>.</value>
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
<value>
  <c>true</c> if required; otherwise, <c>false</c>.</value>
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
    def ToolTip(self)->str:
        """
    <summary>
        Gets or sets the tool tip.
    </summary>
<value>The tool tip.</value>
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
<value>The page.</value>
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


