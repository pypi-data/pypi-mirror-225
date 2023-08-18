from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfButtonField (  PdfAppearanceField) :
    @dispatch
    def __init__(self, page:PdfPageBase, name:str):
        ptrPage:c_void_p = page.Ptr

        GetDllLibPdf().PdfButtonField_CreatePdfButtonFieldPN.argtypes=[c_void_p,c_wchar_p]
        GetDllLibPdf().PdfButtonField_CreatePdfButtonFieldPN.restype = c_void_p
        intPtr = GetDllLibPdf().PdfButtonField_CreatePdfButtonFieldPN(ptrPage,name)
        super(PdfButtonField, self).__init__(intPtr)
    """
    <summary>
        Represents button field in the PDF form.
    </summary>
    """
    @property

    def Text(self)->str:
        """
    <summary>
        Gets or sets the caption text.
    </summary>
<value>The caption text.</value>
        """
        GetDllLibPdf().PdfButtonField_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonField_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfButtonField_get_Text(self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        GetDllLibPdf().PdfButtonField_set_Text.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfButtonField_set_Text(self.Ptr, value)

    @property

    def LayoutMode(self)->'PdfButtonLayoutMode':
        """
    <summary>
        Gets or sets the button layout mode.
    </summary>
        """
        GetDllLibPdf().PdfButtonField_get_LayoutMode.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonField_get_LayoutMode.restype=c_int
        ret = GetDllLibPdf().PdfButtonField_get_LayoutMode(self.Ptr)
        objwraped = PdfButtonLayoutMode(ret)
        return objwraped

    @LayoutMode.setter
    def LayoutMode(self, value:'PdfButtonLayoutMode'):
        GetDllLibPdf().PdfButtonField_set_LayoutMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfButtonField_set_LayoutMode(self.Ptr, value.value)

    @property

    def AlternateText(self)->str:
        """
    <summary>
        Gets or sets the text displayed when the mouse button is pressed within the annotation's active area, only available in Push mode.
    </summary>
        """
        GetDllLibPdf().PdfButtonField_get_AlternateText.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonField_get_AlternateText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfButtonField_get_AlternateText(self.Ptr))
        return ret


    @AlternateText.setter
    def AlternateText(self, value:str):
        GetDllLibPdf().PdfButtonField_set_AlternateText.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfButtonField_set_AlternateText(self.Ptr, value)

    @property

    def RolloverText(self)->str:
        """
    <summary>
        Gets or sets the text displayed when the user rolls the cursor into the annotation's active area without pressing the mouse button, only available in Push mode.
    </summary>
        """
        GetDllLibPdf().PdfButtonField_get_RolloverText.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonField_get_RolloverText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfButtonField_get_RolloverText(self.Ptr))
        return ret


    @RolloverText.setter
    def RolloverText(self, value:str):
        GetDllLibPdf().PdfButtonField_set_RolloverText.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfButtonField_set_RolloverText(self.Ptr, value)

    @property

    def IconLayout(self)->'PdfButtonIconLayout':
        """
    <summary>
        Defining the icon layout.
    </summary>
        """
        GetDllLibPdf().PdfButtonField_get_IconLayout.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonField_get_IconLayout.restype=c_void_p
        intPtr = GetDllLibPdf().PdfButtonField_get_IconLayout(self.Ptr)
        ret = None if intPtr==None else PdfButtonIconLayout(intPtr)
        return ret


    @property

    def Icon(self)->'PdfImage':
        """
    <summary>
        Gets or sets the widget annotation's normal icon displayed when it is not interacting with the user.
    </summary>
        """
        GetDllLibPdf().PdfButtonField_get_Icon.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonField_get_Icon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfButtonField_get_Icon(self.Ptr)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @Icon.setter
    def Icon(self, value:'PdfImage'):
        GetDllLibPdf().PdfButtonField_set_Icon.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfButtonField_set_Icon(self.Ptr, value.Ptr)

    @property

    def AlternateIcon(self)->'PdfImage':
        """
    <summary>
        Gets or sets the widget annotation's alternate icon displayed when the mouse button is pressed within its active area, only available in Push mode.
    </summary>
        """
        GetDllLibPdf().PdfButtonField_get_AlternateIcon.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonField_get_AlternateIcon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfButtonField_get_AlternateIcon(self.Ptr)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @AlternateIcon.setter
    def AlternateIcon(self, value:'PdfImage'):
        GetDllLibPdf().PdfButtonField_set_AlternateIcon.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfButtonField_set_AlternateIcon(self.Ptr, value.Ptr)

    @property

    def RolloverIcon(self)->'PdfImage':
        """
    <summary>
        Gets or sets the widget annotation's rollover icon displayed when the user rolls the cursor into its active area without pressing the mouse button, only available in Push mode.
    </summary>
        """
        GetDllLibPdf().PdfButtonField_get_RolloverIcon.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonField_get_RolloverIcon.restype=c_void_p
        intPtr = GetDllLibPdf().PdfButtonField_get_RolloverIcon(self.Ptr)
        ret = None if intPtr==None else PdfImage(intPtr)
        return ret


    @RolloverIcon.setter
    def RolloverIcon(self, value:'PdfImage'):
        GetDllLibPdf().PdfButtonField_set_RolloverIcon.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfButtonField_set_RolloverIcon(self.Ptr, value.Ptr)

    def AddPrintAction(self):
        """
    <summary>
        Adds Print action to current button field.
            <remarks>Clicking on the specified button will trigger the Print Dialog Box.</remarks></summary>
        """
        GetDllLibPdf().PdfButtonField_AddPrintAction.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonField_AddPrintAction(self.Ptr)

