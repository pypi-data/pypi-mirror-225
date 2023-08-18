from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfTextBoxField (  PdfAppearanceField, IPdfTextBoxField) :
    @dispatch
    def __init__(self, page:PdfPageBase,name:str):
        ptrPage:c_void_p = page.Ptr
        GetDllLibPdf().PdfTextBoxField_CreatePdfTextBoxFieldPN.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfTextBoxField_CreatePdfTextBoxFieldPN.restype = c_void_p
        intPtr = GetDllLibPdf().PdfTextBoxField_CreatePdfTextBoxFieldPN(ptrPage,name)
        super(PdfTextBoxField, self).__init__(intPtr)
    """
    <summary>
        Represents text box field in the PDF form.
    </summary>
    """
    @property

    def Text(self)->str:
        """
    <summary>
        Gets or sets the text.
    </summary>
<value>The text of the text box field.</value>
        """
        GetDllLibPdf().PdfTextBoxField_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextBoxField_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextBoxField_get_Text(self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        GetDllLibPdf().PdfTextBoxField_set_Text.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfTextBoxField_set_Text(self.Ptr, value)

    @property

    def DefaultValue(self)->str:
        """
    <summary>
        Gets or sets the default value.
    </summary>
<value>The default value of the text box field.</value>
        """
        GetDllLibPdf().PdfTextBoxField_get_DefaultValue.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextBoxField_get_DefaultValue.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfTextBoxField_get_DefaultValue(self.Ptr))
        return ret


    @DefaultValue.setter
    def DefaultValue(self, value:str):
        GetDllLibPdf().PdfTextBoxField_set_DefaultValue.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfTextBoxField_set_DefaultValue(self.Ptr, value)

    @property
    def SpellCheck(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether to check spelling.
    </summary>
<value>
  <c>true</c> if check spelling; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfTextBoxField_get_SpellCheck.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextBoxField_get_SpellCheck.restype=c_bool
        ret = GetDllLibPdf().PdfTextBoxField_get_SpellCheck(self.Ptr)
        return ret

    @SpellCheck.setter
    def SpellCheck(self, value:bool):
        GetDllLibPdf().PdfTextBoxField_set_SpellCheck.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTextBoxField_set_SpellCheck(self.Ptr, value)

    @property
    def InsertSpaces(self)->bool:
        """
    <summary>
        Meaningful only if the MaxLength property is set and the Multiline, Password properties are false.
            If set, the field is automatically divided into as many equally spaced positions, or combs, 
            as the value of MaxLength, and the text is laid out into those combs.
    </summary>
<value>
  <c>true</c> if need to insert spaces; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfTextBoxField_get_InsertSpaces.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextBoxField_get_InsertSpaces.restype=c_bool
        ret = GetDllLibPdf().PdfTextBoxField_get_InsertSpaces(self.Ptr)
        return ret

    @InsertSpaces.setter
    def InsertSpaces(self, value:bool):
        GetDllLibPdf().PdfTextBoxField_set_InsertSpaces.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTextBoxField_set_InsertSpaces(self.Ptr, value)

    @property
    def Multiline(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is multiline.
    </summary>
<value>
  <c>true</c> if multiline; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfTextBoxField_get_Multiline.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextBoxField_get_Multiline.restype=c_bool
        ret = GetDllLibPdf().PdfTextBoxField_get_Multiline(self.Ptr)
        return ret

    @Multiline.setter
    def Multiline(self, value:bool):
        GetDllLibPdf().PdfTextBoxField_set_Multiline.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTextBoxField_set_Multiline(self.Ptr, value)

    @property
    def Password(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is password field.
    </summary>
<value>
  <c>true</c> if password field; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfTextBoxField_get_Password.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextBoxField_get_Password.restype=c_bool
        ret = GetDllLibPdf().PdfTextBoxField_get_Password(self.Ptr)
        return ret

    @Password.setter
    def Password(self, value:bool):
        GetDllLibPdf().PdfTextBoxField_set_Password.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTextBoxField_set_Password(self.Ptr, value)

    @property
    def Scrollable(self)->bool:
        """
    <summary>
        Gets or sets a value indicating whether this  is scrollable.
    </summary>
<value>
  <c>true</c> if scrollable; otherwise, <c>false</c>.</value>
        """
        GetDllLibPdf().PdfTextBoxField_get_Scrollable.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextBoxField_get_Scrollable.restype=c_bool
        ret = GetDllLibPdf().PdfTextBoxField_get_Scrollable(self.Ptr)
        return ret

    @Scrollable.setter
    def Scrollable(self, value:bool):
        GetDllLibPdf().PdfTextBoxField_set_Scrollable.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PdfTextBoxField_set_Scrollable(self.Ptr, value)

    @property
    def MaxLength(self)->int:
        """
    <summary>
        Gets or sets the maximum number of characters that can be entered in the text box.
    </summary>
<value>An integer value specifying the maximum number of characters that can be entered in the text box.</value>
        """
        GetDllLibPdf().PdfTextBoxField_get_MaxLength.argtypes=[c_void_p]
        GetDllLibPdf().PdfTextBoxField_get_MaxLength.restype=c_int
        ret = GetDllLibPdf().PdfTextBoxField_get_MaxLength(self.Ptr)
        return ret

    @MaxLength.setter
    def MaxLength(self, value:int):
        GetDllLibPdf().PdfTextBoxField_set_MaxLength.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfTextBoxField_set_MaxLength(self.Ptr, value)

