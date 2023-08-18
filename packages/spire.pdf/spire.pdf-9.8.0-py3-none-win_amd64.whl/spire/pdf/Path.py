from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Path (SpireObject) :
    """
<remarks />
    """
    @property

    def PathRenderTransform(self)->'Transform':
        """
<remarks />
        """
        GetDllLibPdf().Path_get_PathRenderTransform.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_PathRenderTransform.restype=c_void_p
        intPtr = GetDllLibPdf().Path_get_PathRenderTransform(self.Ptr)
        ret = None if intPtr==None else Transform(intPtr)
        return ret


    @PathRenderTransform.setter
    def PathRenderTransform(self, value:'Transform'):
        GetDllLibPdf().Path_set_PathRenderTransform.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Path_set_PathRenderTransform(self.Ptr, value.Ptr)

    @property

    def PathClip(self)->'Geometry':
        """
<remarks />
        """
        GetDllLibPdf().Path_get_PathClip.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_PathClip.restype=c_void_p
        intPtr = GetDllLibPdf().Path_get_PathClip(self.Ptr)
        ret = None if intPtr==None else Geometry(intPtr)
        return ret


    @PathClip.setter
    def PathClip(self, value:'Geometry'):
        GetDllLibPdf().Path_set_PathClip.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Path_set_PathClip(self.Ptr, value.Ptr)

    @property

    def PathOpacityMask(self)->'Brush':
        """
<remarks />
        """
        GetDllLibPdf().Path_get_PathOpacityMask.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_PathOpacityMask.restype=c_void_p
        intPtr = GetDllLibPdf().Path_get_PathOpacityMask(self.Ptr)
        ret = None if intPtr==None else Brush(intPtr)
        return ret


    @PathOpacityMask.setter
    def PathOpacityMask(self, value:'Brush'):
        GetDllLibPdf().Path_set_PathOpacityMask.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Path_set_PathOpacityMask(self.Ptr, value.Ptr)

    @property

    def PathFill(self)->'Brush':
        """
<remarks />
        """
        GetDllLibPdf().Path_get_PathFill.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_PathFill.restype=c_void_p
        intPtr = GetDllLibPdf().Path_get_PathFill(self.Ptr)
        ret = None if intPtr==None else Brush(intPtr)
        return ret


    @PathFill.setter
    def PathFill(self, value:'Brush'):
        GetDllLibPdf().Path_set_PathFill.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Path_set_PathFill(self.Ptr, value.Ptr)

    @property

    def PathStroke(self)->'Brush':
        """
<remarks />
        """
        GetDllLibPdf().Path_get_PathStroke.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_PathStroke.restype=c_void_p
        intPtr = GetDllLibPdf().Path_get_PathStroke(self.Ptr)
        ret = None if intPtr==None else Brush(intPtr)
        return ret


    @PathStroke.setter
    def PathStroke(self, value:'Brush'):
        GetDllLibPdf().Path_set_PathStroke.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Path_set_PathStroke(self.Ptr, value.Ptr)

    @property

    def PathData(self)->'Geometry':
        """
<remarks />
        """
        GetDllLibPdf().Path_get_PathData.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_PathData.restype=c_void_p
        intPtr = GetDllLibPdf().Path_get_PathData(self.Ptr)
        ret = None if intPtr==None else Geometry(intPtr)
        return ret


    @PathData.setter
    def PathData(self, value:'Geometry'):
        GetDllLibPdf().Path_set_PathData.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Path_set_PathData(self.Ptr, value.Ptr)

    @property

    def Data(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_Data.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_Data.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_Data(self.Ptr))
        return ret


    @Data.setter
    def Data(self, value:str):
        GetDllLibPdf().Path_set_Data.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_Data(self.Ptr, value)

    @property

    def Fill(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_Fill.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_Fill.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_Fill(self.Ptr))
        return ret


    @Fill.setter
    def Fill(self, value:str):
        GetDllLibPdf().Path_set_Fill.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_Fill(self.Ptr, value)

    @property

    def RenderTransform(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_RenderTransform.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_RenderTransform.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_RenderTransform(self.Ptr))
        return ret


    @RenderTransform.setter
    def RenderTransform(self, value:str):
        GetDllLibPdf().Path_set_RenderTransform.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_RenderTransform(self.Ptr, value)

    @property

    def Clip(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_Clip.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_Clip.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_Clip(self.Ptr))
        return ret


    @Clip.setter
    def Clip(self, value:str):
        GetDllLibPdf().Path_set_Clip.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_Clip(self.Ptr, value)

    @property
    def Opacity(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_Opacity.restype=c_double
        ret = GetDllLibPdf().Path_get_Opacity(self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibPdf().Path_set_Opacity.argtypes=[c_void_p, c_double]
        GetDllLibPdf().Path_set_Opacity(self.Ptr, value)

    @property

    def OpacityMask(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_OpacityMask.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_OpacityMask.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_OpacityMask(self.Ptr))
        return ret


    @OpacityMask.setter
    def OpacityMask(self, value:str):
        GetDllLibPdf().Path_set_OpacityMask.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_OpacityMask(self.Ptr, value)

    @property

    def Stroke(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_Stroke.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_Stroke.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_Stroke(self.Ptr))
        return ret


    @Stroke.setter
    def Stroke(self, value:str):
        GetDllLibPdf().Path_set_Stroke.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_Stroke(self.Ptr, value)

    @property

    def StrokeDashArray(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_StrokeDashArray.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_StrokeDashArray.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_StrokeDashArray(self.Ptr))
        return ret


    @StrokeDashArray.setter
    def StrokeDashArray(self, value:str):
        GetDllLibPdf().Path_set_StrokeDashArray.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_StrokeDashArray(self.Ptr, value)

    @property

    def StrokeDashCap(self)->'DashCap':
        """
<remarks />
        """
        GetDllLibPdf().Path_get_StrokeDashCap.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_StrokeDashCap.restype=c_int
        ret = GetDllLibPdf().Path_get_StrokeDashCap(self.Ptr)
        objwraped = DashCap(ret)
        return objwraped

    @StrokeDashCap.setter
    def StrokeDashCap(self, value:'DashCap'):
        GetDllLibPdf().Path_set_StrokeDashCap.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Path_set_StrokeDashCap(self.Ptr, value.value)

    @property
    def StrokeDashOffset(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_StrokeDashOffset.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_StrokeDashOffset.restype=c_double
        ret = GetDllLibPdf().Path_get_StrokeDashOffset(self.Ptr)
        return ret

    @StrokeDashOffset.setter
    def StrokeDashOffset(self, value:float):
        GetDllLibPdf().Path_set_StrokeDashOffset.argtypes=[c_void_p, c_double]
        GetDllLibPdf().Path_set_StrokeDashOffset(self.Ptr, value)

    @property

    def StrokeEndLineCap(self)->'LineCap':
        """
<remarks />
        """
        GetDllLibPdf().Path_get_StrokeEndLineCap.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_StrokeEndLineCap.restype=c_int
        ret = GetDllLibPdf().Path_get_StrokeEndLineCap(self.Ptr)
        objwraped = LineCap(ret)
        return objwraped

    @StrokeEndLineCap.setter
    def StrokeEndLineCap(self, value:'LineCap'):
        GetDllLibPdf().Path_set_StrokeEndLineCap.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Path_set_StrokeEndLineCap(self.Ptr, value.value)

    @property

    def StrokeStartLineCap(self)->'LineCap':
        """
<remarks />
        """
        GetDllLibPdf().Path_get_StrokeStartLineCap.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_StrokeStartLineCap.restype=c_int
        ret = GetDllLibPdf().Path_get_StrokeStartLineCap(self.Ptr)
        objwraped = LineCap(ret)
        return objwraped

    @StrokeStartLineCap.setter
    def StrokeStartLineCap(self, value:'LineCap'):
        GetDllLibPdf().Path_set_StrokeStartLineCap.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Path_set_StrokeStartLineCap(self.Ptr, value.value)

    @property

    def StrokeLineJoin(self)->'LineJoin':
        """
<remarks />
        """
        GetDllLibPdf().Path_get_StrokeLineJoin.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_StrokeLineJoin.restype=c_int
        ret = GetDllLibPdf().Path_get_StrokeLineJoin(self.Ptr)
        objwraped = LineJoin(ret)
        return objwraped

    @StrokeLineJoin.setter
    def StrokeLineJoin(self, value:'LineJoin'):
        GetDllLibPdf().Path_set_StrokeLineJoin.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Path_set_StrokeLineJoin(self.Ptr, value.value)

    @property
    def StrokeMiterLimit(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_StrokeMiterLimit.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_StrokeMiterLimit.restype=c_double
        ret = GetDllLibPdf().Path_get_StrokeMiterLimit(self.Ptr)
        return ret

    @StrokeMiterLimit.setter
    def StrokeMiterLimit(self, value:float):
        GetDllLibPdf().Path_set_StrokeMiterLimit.argtypes=[c_void_p, c_double]
        GetDllLibPdf().Path_set_StrokeMiterLimit(self.Ptr, value)

    @property
    def StrokeThickness(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_StrokeThickness.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_StrokeThickness.restype=c_double
        ret = GetDllLibPdf().Path_get_StrokeThickness(self.Ptr)
        return ret

    @StrokeThickness.setter
    def StrokeThickness(self, value:float):
        GetDllLibPdf().Path_set_StrokeThickness.argtypes=[c_void_p, c_double]
        GetDllLibPdf().Path_set_StrokeThickness(self.Ptr, value)

    @property

    def Name(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_Name(self.Ptr))
        return ret


    @Name.setter
    def Name(self, value:str):
        GetDllLibPdf().Path_set_Name.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_Name(self.Ptr, value)

    @property

    def FixedPageNavigateUri(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_FixedPageNavigateUri.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_FixedPageNavigateUri.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_FixedPageNavigateUri(self.Ptr))
        return ret


    @FixedPageNavigateUri.setter
    def FixedPageNavigateUri(self, value:str):
        GetDllLibPdf().Path_set_FixedPageNavigateUri.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_FixedPageNavigateUri(self.Ptr, value)

    @property

    def lang(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_lang.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_lang.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_lang(self.Ptr))
        return ret


    @lang.setter
    def lang(self, value:str):
        GetDllLibPdf().Path_set_lang.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_lang(self.Ptr, value)

    @property

    def Key(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_Key.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_Key.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_Key(self.Ptr))
        return ret


    @Key.setter
    def Key(self, value:str):
        GetDllLibPdf().Path_set_Key.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_Key(self.Ptr, value)

    @property

    def AutomationPropertiesName(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_AutomationPropertiesName.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_AutomationPropertiesName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_AutomationPropertiesName(self.Ptr))
        return ret


    @AutomationPropertiesName.setter
    def AutomationPropertiesName(self, value:str):
        GetDllLibPdf().Path_set_AutomationPropertiesName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_AutomationPropertiesName(self.Ptr, value)

    @property

    def AutomationPropertiesHelpText(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_AutomationPropertiesHelpText.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_AutomationPropertiesHelpText.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Path_get_AutomationPropertiesHelpText(self.Ptr))
        return ret


    @AutomationPropertiesHelpText.setter
    def AutomationPropertiesHelpText(self, value:str):
        GetDllLibPdf().Path_set_AutomationPropertiesHelpText.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Path_set_AutomationPropertiesHelpText(self.Ptr, value)

    @property
    def SnapsToDevicePixels(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_SnapsToDevicePixels.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_SnapsToDevicePixels.restype=c_bool
        ret = GetDllLibPdf().Path_get_SnapsToDevicePixels(self.Ptr)
        return ret

    @SnapsToDevicePixels.setter
    def SnapsToDevicePixels(self, value:bool):
        GetDllLibPdf().Path_set_SnapsToDevicePixels.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().Path_set_SnapsToDevicePixels(self.Ptr, value)

    @property
    def SnapsToDevicePixelsSpecified(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().Path_get_SnapsToDevicePixelsSpecified.argtypes=[c_void_p]
        GetDllLibPdf().Path_get_SnapsToDevicePixelsSpecified.restype=c_bool
        ret = GetDllLibPdf().Path_get_SnapsToDevicePixelsSpecified(self.Ptr)
        return ret

    @SnapsToDevicePixelsSpecified.setter
    def SnapsToDevicePixelsSpecified(self, value:bool):
        GetDllLibPdf().Path_set_SnapsToDevicePixelsSpecified.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().Path_set_SnapsToDevicePixelsSpecified(self.Ptr, value)

