from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfExtendedAppearance (SpireObject) :
    """
    <summary>
        Represents extended appearance of the annotation. It has two states such as On state and Off state.
    </summary>
    """
    @property

    def Normal(self)->'PdfAppearanceState':
        """
    <summary>
        Gets the normal appearance of the annotation.
    </summary>
<value>The  object specifies the normal appearance of the annotation.</value>
        """
        GetDllLibPdf().PdfExtendedAppearance_get_Normal.argtypes=[c_void_p]
        GetDllLibPdf().PdfExtendedAppearance_get_Normal.restype=c_void_p
        intPtr = GetDllLibPdf().PdfExtendedAppearance_get_Normal(self.Ptr)
        ret = None if intPtr==None else PdfAppearanceState(intPtr)
        return ret


    @property

    def MouseHover(self)->'PdfAppearanceState':
        """
    <summary>
        Gets the appearance when mouse is hovered.
    </summary>
<value>The  object specifies the annotation appearance when the mouse is hovered on it.</value>
        """
        GetDllLibPdf().PdfExtendedAppearance_get_MouseHover.argtypes=[c_void_p]
        GetDllLibPdf().PdfExtendedAppearance_get_MouseHover.restype=c_void_p
        intPtr = GetDllLibPdf().PdfExtendedAppearance_get_MouseHover(self.Ptr)
        ret = None if intPtr==None else PdfAppearanceState(intPtr)
        return ret


    @property

    def Pressed(self)->'PdfAppearanceState':
        """
    <summary>
        Gets the pressed state annotation.
    </summary>
<value>The appearance in pressed state.</value>
        """
        GetDllLibPdf().PdfExtendedAppearance_get_Pressed.argtypes=[c_void_p]
        GetDllLibPdf().PdfExtendedAppearance_get_Pressed.restype=c_void_p
        intPtr = GetDllLibPdf().PdfExtendedAppearance_get_Pressed(self.Ptr)
        ret = None if intPtr==None else PdfAppearanceState(intPtr)
        return ret


