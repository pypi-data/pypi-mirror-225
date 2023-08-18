from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfButtonWidgetFieldWidget (  PdfStyledFieldWidget) :
    """
    <summary>
        Represents a button field of an existing PDF document`s form.
    </summary>
    """
    @property

    def Text(self)->str:
        """
    <summary>
        Gets or sets the caption text.
    </summary>
<value>A string value specifying the caption of the button.</value>
        """
        GetDllLibPdf().PdfButtonWidgetFieldWidget_get_Text.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonWidgetFieldWidget_get_Text.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfButtonWidgetFieldWidget_get_Text(self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        GetDllLibPdf().PdfButtonWidgetFieldWidget_set_Text.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfButtonWidgetFieldWidget_set_Text(self.Ptr, value)

    @property

    def WidgetItems(self)->'PdfButtonWidgetItemCollection':
        """
    <summary>
        Gets the collection of button items.
    </summary>
        """
        GetDllLibPdf().PdfButtonWidgetFieldWidget_get_WidgetItems.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonWidgetFieldWidget_get_WidgetItems.restype=c_void_p
        intPtr = GetDllLibPdf().PdfButtonWidgetFieldWidget_get_WidgetItems(self.Ptr)
        ret = None if intPtr==None else PdfButtonWidgetItemCollection(intPtr)
        return ret


    @property

    def IconLayout(self)->'PdfButtonIconLayout':
        """
    <summary>
        Defining the icon layout.
    </summary>
        """
        GetDllLibPdf().PdfButtonWidgetFieldWidget_get_IconLayout.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonWidgetFieldWidget_get_IconLayout.restype=c_void_p
        intPtr = GetDllLibPdf().PdfButtonWidgetFieldWidget_get_IconLayout(self.Ptr)
        ret = None if intPtr==None else PdfButtonIconLayout(intPtr)
        return ret



    def SetButtonImage(self ,image:'PdfImage'):
        """
    <summary>
        need replace image
    </summary>
    <param name="image"></param>
        """
        intPtrimage:c_void_p = image.Ptr

        GetDllLibPdf().PdfButtonWidgetFieldWidget_SetButtonImage.argtypes=[c_void_p ,c_void_p]
        GetDllLibPdf().PdfButtonWidgetFieldWidget_SetButtonImage(self.Ptr, intPtrimage)

    def AddPrintAction(self):
        """
    <summary>
        Adds Print action to current button field.</summary>
<remarks>Clicking on the specified button will trigger the Print Dialog Box.</remarks>
        """
        GetDllLibPdf().PdfButtonWidgetFieldWidget_AddPrintAction.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonWidgetFieldWidget_AddPrintAction(self.Ptr)

    def ObjectID(self)->int:
        """
    <summary>
        Form field identifier
    </summary>
        """
        GetDllLibPdf().PdfButtonWidgetFieldWidget_ObjectID.argtypes=[c_void_p]
        GetDllLibPdf().PdfButtonWidgetFieldWidget_ObjectID.restype=c_int
        ret = GetDllLibPdf().PdfButtonWidgetFieldWidget_ObjectID(self.Ptr)
        return ret

