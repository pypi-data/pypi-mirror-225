from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAppearanceState (SpireObject) :
    """
    <summary>
        Represents the states of an annotation's appearance.
    </summary>
    """
    @property

    def On(self)->'PdfTemplate':
        """
    <summary>
        Gets or sets the active state template.
    </summary>
<value>The  object specifies an active state template.</value>
        """
        GetDllLibPdf().PdfAppearanceState_get_On.argtypes=[c_void_p]
        GetDllLibPdf().PdfAppearanceState_get_On.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAppearanceState_get_On(self.Ptr)
        ret = None if intPtr==None else PdfTemplate(intPtr)
        return ret


    @On.setter
    def On(self, value:'PdfTemplate'):
        GetDllLibPdf().PdfAppearanceState_set_On.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAppearanceState_set_On(self.Ptr, value.Ptr)

    @property

    def Off(self)->'PdfTemplate':
        """
    <summary>
        Gets or sets the inactive state.
    </summary>
<value>The  object specifies an inactive state template.</value>
        """
        GetDllLibPdf().PdfAppearanceState_get_Off.argtypes=[c_void_p]
        GetDllLibPdf().PdfAppearanceState_get_Off.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAppearanceState_get_Off(self.Ptr)
        ret = None if intPtr==None else PdfTemplate(intPtr)
        return ret


    @Off.setter
    def Off(self, value:'PdfTemplate'):
        GetDllLibPdf().PdfAppearanceState_set_Off.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAppearanceState_set_Off(self.Ptr, value.Ptr)

    @property

    def OnMappingName(self)->str:
        """
    <summary>
        Gets or sets the mapping name of the active state.
    </summary>
<value>String specifies the mapping name of the active state.</value>
        """
        GetDllLibPdf().PdfAppearanceState_get_OnMappingName.argtypes=[c_void_p]
        GetDllLibPdf().PdfAppearanceState_get_OnMappingName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfAppearanceState_get_OnMappingName(self.Ptr))
        return ret


    @OnMappingName.setter
    def OnMappingName(self, value:str):
        GetDllLibPdf().PdfAppearanceState_set_OnMappingName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfAppearanceState_set_OnMappingName(self.Ptr, value)

    @property

    def OffMappingName(self)->str:
        """
    <summary>
        Gets or sets the mapping name of the inactive state.
    </summary>
<value>String specifies the mapping name of the inactive state.</value>
        """
        GetDllLibPdf().PdfAppearanceState_get_OffMappingName.argtypes=[c_void_p]
        GetDllLibPdf().PdfAppearanceState_get_OffMappingName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PdfAppearanceState_get_OffMappingName(self.Ptr))
        return ret


    @OffMappingName.setter
    def OffMappingName(self, value:str):
        GetDllLibPdf().PdfAppearanceState_set_OffMappingName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PdfAppearanceState_set_OffMappingName(self.Ptr, value)

