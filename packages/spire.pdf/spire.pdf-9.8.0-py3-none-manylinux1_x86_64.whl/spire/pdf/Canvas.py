from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Canvas (SpireObject) :
    """
<remarks />
    """
    @property

    def CanvasResources(self)->'Resources':
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_CanvasResources.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_CanvasResources.restype=c_void_p
        intPtr = GetDllLibPdf().Canvas_get_CanvasResources(self.Ptr)
        ret = None if intPtr==None else Resources(intPtr)
        return ret


    @CanvasResources.setter
    def CanvasResources(self, value:'Resources'):
        GetDllLibPdf().Canvas_set_CanvasResources.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Canvas_set_CanvasResources(self.Ptr, value.Ptr)

    @property

    def CanvasRenderTransform(self)->'Transform':
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_CanvasRenderTransform.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_CanvasRenderTransform.restype=c_void_p
        intPtr = GetDllLibPdf().Canvas_get_CanvasRenderTransform(self.Ptr)
        ret = None if intPtr==None else Transform(intPtr)
        return ret


    @CanvasRenderTransform.setter
    def CanvasRenderTransform(self, value:'Transform'):
        GetDllLibPdf().Canvas_set_CanvasRenderTransform.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Canvas_set_CanvasRenderTransform(self.Ptr, value.Ptr)

    @property

    def CanvasClip(self)->'Geometry':
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_CanvasClip.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_CanvasClip.restype=c_void_p
        intPtr = GetDllLibPdf().Canvas_get_CanvasClip(self.Ptr)
        ret = None if intPtr==None else Geometry(intPtr)
        return ret


    @CanvasClip.setter
    def CanvasClip(self, value:'Geometry'):
        GetDllLibPdf().Canvas_set_CanvasClip.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Canvas_set_CanvasClip(self.Ptr, value.Ptr)

    @property

    def CanvasOpacityMask(self)->'Brush':
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_CanvasOpacityMask.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_CanvasOpacityMask.restype=c_void_p
        intPtr = GetDllLibPdf().Canvas_get_CanvasOpacityMask(self.Ptr)
        ret = None if intPtr==None else Brush(intPtr)
        return ret


    @CanvasOpacityMask.setter
    def CanvasOpacityMask(self, value:'Brush'):
        GetDllLibPdf().Canvas_set_CanvasOpacityMask.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Canvas_set_CanvasOpacityMask(self.Ptr, value.Ptr)

    @property

    def Items(self)->List['SpireObject']:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_Items.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().Canvas_get_Items(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, SpireObject)
        return ret

    @Items.setter
    def Items(self, value:List['SpireObject']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().Canvas_set_Items.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().Canvas_set_Items(self.Ptr, vArray, vCount)

    @property

    def RenderTransform(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_RenderTransform.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_RenderTransform.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Canvas_get_RenderTransform(self.Ptr))
        return ret


    @RenderTransform.setter
    def RenderTransform(self, value:str):
        GetDllLibPdf().Canvas_set_RenderTransform.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Canvas_set_RenderTransform(self.Ptr, value)

    @property

    def Clip(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_Clip.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_Clip.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Canvas_get_Clip(self.Ptr))
        return ret


    @Clip.setter
    def Clip(self, value:str):
        GetDllLibPdf().Canvas_set_Clip.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Canvas_set_Clip(self.Ptr, value)

    @property
    def Opacity(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_Opacity.restype=c_double
        ret = GetDllLibPdf().Canvas_get_Opacity(self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibPdf().Canvas_set_Opacity.argtypes=[c_void_p, c_double]
        GetDllLibPdf().Canvas_set_Opacity(self.Ptr, value)

    @property

    def OpacityMask(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_OpacityMask.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_OpacityMask.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Canvas_get_OpacityMask(self.Ptr))
        return ret


    @OpacityMask.setter
    def OpacityMask(self, value:str):
        GetDllLibPdf().Canvas_set_OpacityMask.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Canvas_set_OpacityMask(self.Ptr, value)

    @property

    def Name(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Canvas_get_Name(self.Ptr))
        return ret


    @Name.setter
    def Name(self, value:str):
        GetDllLibPdf().Canvas_set_Name.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Canvas_set_Name(self.Ptr, value)

    @property

    def RenderOptionsEdgeMode(self)->'EdgeMode':
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_RenderOptionsEdgeMode.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_RenderOptionsEdgeMode.restype=c_int
        ret = GetDllLibPdf().Canvas_get_RenderOptionsEdgeMode(self.Ptr)
        objwraped = EdgeMode(ret)
        return objwraped

    @RenderOptionsEdgeMode.setter
    def RenderOptionsEdgeMode(self, value:'EdgeMode'):
        GetDllLibPdf().Canvas_set_RenderOptionsEdgeMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Canvas_set_RenderOptionsEdgeMode(self.Ptr, value.value)

    @property
    def RenderOptionsEdgeModeSpecified(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_RenderOptionsEdgeModeSpecified.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_RenderOptionsEdgeModeSpecified.restype=c_bool
        ret = GetDllLibPdf().Canvas_get_RenderOptionsEdgeModeSpecified(self.Ptr)
        return ret

    @RenderOptionsEdgeModeSpecified.setter
    def RenderOptionsEdgeModeSpecified(self, value:bool):
        GetDllLibPdf().Canvas_set_RenderOptionsEdgeModeSpecified.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().Canvas_set_RenderOptionsEdgeModeSpecified(self.Ptr, value)

    @property

    def FixedPageNavigateUri(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_FixedPageNavigateUri.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_FixedPageNavigateUri.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Canvas_get_FixedPageNavigateUri(self.Ptr))
        return ret


    @FixedPageNavigateUri.setter
    def FixedPageNavigateUri(self, value:str):
        GetDllLibPdf().Canvas_set_FixedPageNavigateUri.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Canvas_set_FixedPageNavigateUri(self.Ptr, value)

    @property

    def lang(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_lang.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_lang.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Canvas_get_lang(self.Ptr))
        return ret


    @lang.setter
    def lang(self, value:str):
        GetDllLibPdf().Canvas_set_lang.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Canvas_set_lang(self.Ptr, value)

    @property

    def Key(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_Key.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_Key.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Canvas_get_Key(self.Ptr))
        return ret


    @Key.setter
    def Key(self, value:str):
        GetDllLibPdf().Canvas_set_Key.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Canvas_set_Key(self.Ptr, value)

    @property

    def AutomationPropertiesName(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_AutomationPropertiesName.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_AutomationPropertiesName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Canvas_get_AutomationPropertiesName(self.Ptr))
        return ret


    @AutomationPropertiesName.setter
    def AutomationPropertiesName(self, value:str):
        GetDllLibPdf().Canvas_set_AutomationPropertiesName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Canvas_set_AutomationPropertiesName(self.Ptr, value)

    @property

    def AutomationPropertiesHelpText(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Canvas_get_AutomationPropertiesHelpText.argtypes=[c_void_p]
        GetDllLibPdf().Canvas_get_AutomationPropertiesHelpText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Canvas_get_AutomationPropertiesHelpText(self.Ptr))
        return ret


    @AutomationPropertiesHelpText.setter
    def AutomationPropertiesHelpText(self, value:str):
        GetDllLibPdf().Canvas_set_AutomationPropertiesHelpText.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Canvas_set_AutomationPropertiesHelpText(self.Ptr, value)

