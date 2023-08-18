from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class VisualBrush (SpireObject) :
    """
<remarks />
    """
    @property

    def VisualBrushTransform(self)->'Transform':
        """
<remarks />
        """
        GetDllLibPdf().VisualBrush_get_VisualBrushTransform.argtypes=[c_void_p]
        GetDllLibPdf().VisualBrush_get_VisualBrushTransform.restype=c_void_p
        intPtr = GetDllLibPdf().VisualBrush_get_VisualBrushTransform(self.Ptr)
        ret = None if intPtr==None else Transform(intPtr)
        return ret


    @VisualBrushTransform.setter
    def VisualBrushTransform(self, value:'Transform'):
        GetDllLibPdf().VisualBrush_set_VisualBrushTransform.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().VisualBrush_set_VisualBrushTransform(self.Ptr, value.Ptr)

    @property

    def VisualBrushVisual(self)->'Visual':
        """
<remarks />
        """
        GetDllLibPdf().VisualBrush_get_VisualBrushVisual.argtypes=[c_void_p]
        GetDllLibPdf().VisualBrush_get_VisualBrushVisual.restype=c_void_p
        intPtr = GetDllLibPdf().VisualBrush_get_VisualBrushVisual(self.Ptr)
        ret = None if intPtr==None else Visual(intPtr)
        return ret


    @VisualBrushVisual.setter
    def VisualBrushVisual(self, value:'Visual'):
        GetDllLibPdf().VisualBrush_set_VisualBrushVisual.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().VisualBrush_set_VisualBrushVisual(self.Ptr, value.Ptr)

    @property
    def Opacity(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().VisualBrush_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().VisualBrush_get_Opacity.restype=c_double
        ret = GetDllLibPdf().VisualBrush_get_Opacity(self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibPdf().VisualBrush_set_Opacity.argtypes=[c_void_p, c_double]
        GetDllLibPdf().VisualBrush_set_Opacity(self.Ptr, value)

    @property

    def Key(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().VisualBrush_get_Key.argtypes=[c_void_p]
        GetDllLibPdf().VisualBrush_get_Key.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().VisualBrush_get_Key(self.Ptr))
        return ret


    @Key.setter
    def Key(self, value:str):
        GetDllLibPdf().VisualBrush_set_Key.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().VisualBrush_set_Key(self.Ptr, value)

    @property

    def Transform(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().VisualBrush_get_Transform.argtypes=[c_void_p]
        GetDllLibPdf().VisualBrush_get_Transform.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().VisualBrush_get_Transform(self.Ptr))
        return ret


    @Transform.setter
    def Transform(self, value:str):
        GetDllLibPdf().VisualBrush_set_Transform.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().VisualBrush_set_Transform(self.Ptr, value)

    @property

    def Viewbox(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().VisualBrush_get_Viewbox.argtypes=[c_void_p]
        GetDllLibPdf().VisualBrush_get_Viewbox.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().VisualBrush_get_Viewbox(self.Ptr))
        return ret


    @Viewbox.setter
    def Viewbox(self, value:str):
        GetDllLibPdf().VisualBrush_set_Viewbox.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().VisualBrush_set_Viewbox(self.Ptr, value)

    @property

    def Viewport(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().VisualBrush_get_Viewport.argtypes=[c_void_p]
        GetDllLibPdf().VisualBrush_get_Viewport.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().VisualBrush_get_Viewport(self.Ptr))
        return ret


    @Viewport.setter
    def Viewport(self, value:str):
        GetDllLibPdf().VisualBrush_set_Viewport.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().VisualBrush_set_Viewport(self.Ptr, value)

    @property

    def TileMode(self)->'TileMode':
        """
<remarks />
        """
        GetDllLibPdf().VisualBrush_get_TileMode.argtypes=[c_void_p]
        GetDllLibPdf().VisualBrush_get_TileMode.restype=c_int
        ret = GetDllLibPdf().VisualBrush_get_TileMode(self.Ptr)
        objwraped = TileMode(ret)
        return objwraped

    @TileMode.setter
    def TileMode(self, value:'TileMode'):
        GetDllLibPdf().VisualBrush_set_TileMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().VisualBrush_set_TileMode(self.Ptr, value.value)

    @property

    def ViewboxUnits(self)->'ViewUnits':
        """
<remarks />
        """
        GetDllLibPdf().VisualBrush_get_ViewboxUnits.argtypes=[c_void_p]
        GetDllLibPdf().VisualBrush_get_ViewboxUnits.restype=c_int
        ret = GetDllLibPdf().VisualBrush_get_ViewboxUnits(self.Ptr)
        objwraped = ViewUnits(ret)
        return objwraped

    @ViewboxUnits.setter
    def ViewboxUnits(self, value:'ViewUnits'):
        GetDllLibPdf().VisualBrush_set_ViewboxUnits.argtypes=[c_void_p, c_int]
        GetDllLibPdf().VisualBrush_set_ViewboxUnits(self.Ptr, value.value)

    @property

    def ViewportUnits(self)->'ViewUnits':
        """
<remarks />
        """
        GetDllLibPdf().VisualBrush_get_ViewportUnits.argtypes=[c_void_p]
        GetDllLibPdf().VisualBrush_get_ViewportUnits.restype=c_int
        ret = GetDllLibPdf().VisualBrush_get_ViewportUnits(self.Ptr)
        objwraped = ViewUnits(ret)
        return objwraped

    @ViewportUnits.setter
    def ViewportUnits(self, value:'ViewUnits'):
        GetDllLibPdf().VisualBrush_set_ViewportUnits.argtypes=[c_void_p, c_int]
        GetDllLibPdf().VisualBrush_set_ViewportUnits(self.Ptr, value.value)

    @property

    def Visual(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().VisualBrush_get_Visual.argtypes=[c_void_p]
        GetDllLibPdf().VisualBrush_get_Visual.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().VisualBrush_get_Visual(self.Ptr))
        return ret


    @Visual.setter
    def Visual(self, value:str):
        GetDllLibPdf().VisualBrush_set_Visual.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().VisualBrush_set_Visual(self.Ptr, value)

