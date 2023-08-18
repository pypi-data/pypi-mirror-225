from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Glyphs (SpireObject) :
    """
<remarks />
    """
    @property

    def GlyphsRenderTransform(self)->'Transform':
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_GlyphsRenderTransform.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_GlyphsRenderTransform.restype=c_void_p
        intPtr = GetDllLibPdf().Glyphs_get_GlyphsRenderTransform(self.Ptr)
        ret = None if intPtr==None else Transform(intPtr)
        return ret


    @GlyphsRenderTransform.setter
    def GlyphsRenderTransform(self, value:'Transform'):
        GetDllLibPdf().Glyphs_set_GlyphsRenderTransform.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Glyphs_set_GlyphsRenderTransform(self.Ptr, value.Ptr)

    @property

    def GlyphsClip(self)->'Geometry':
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_GlyphsClip.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_GlyphsClip.restype=c_void_p
        intPtr = GetDllLibPdf().Glyphs_get_GlyphsClip(self.Ptr)
        ret = None if intPtr==None else Geometry(intPtr)
        return ret


    @GlyphsClip.setter
    def GlyphsClip(self, value:'Geometry'):
        GetDllLibPdf().Glyphs_set_GlyphsClip.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Glyphs_set_GlyphsClip(self.Ptr, value.Ptr)

    @property

    def GlyphsOpacityMask(self)->'Brush':
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_GlyphsOpacityMask.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_GlyphsOpacityMask.restype=c_void_p
        intPtr = GetDllLibPdf().Glyphs_get_GlyphsOpacityMask(self.Ptr)
        ret = None if intPtr==None else Brush(intPtr)
        return ret


    @GlyphsOpacityMask.setter
    def GlyphsOpacityMask(self, value:'Brush'):
        GetDllLibPdf().Glyphs_set_GlyphsOpacityMask.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Glyphs_set_GlyphsOpacityMask(self.Ptr, value.Ptr)

    @property

    def GlyphsFill(self)->'Brush':
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_GlyphsFill.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_GlyphsFill.restype=c_void_p
        intPtr = GetDllLibPdf().Glyphs_get_GlyphsFill(self.Ptr)
        ret = None if intPtr==None else Brush(intPtr)
        return ret


    @GlyphsFill.setter
    def GlyphsFill(self, value:'Brush'):
        GetDllLibPdf().Glyphs_set_GlyphsFill.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Glyphs_set_GlyphsFill(self.Ptr, value.Ptr)

    @property

    def BidiLevel(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_BidiLevel.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_BidiLevel.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_BidiLevel(self.Ptr))
        return ret


    @BidiLevel.setter
    def BidiLevel(self, value:str):
        GetDllLibPdf().Glyphs_set_BidiLevel.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_BidiLevel(self.Ptr, value)

    @property

    def CaretStops(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_CaretStops.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_CaretStops.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_CaretStops(self.Ptr))
        return ret


    @CaretStops.setter
    def CaretStops(self, value:str):
        GetDllLibPdf().Glyphs_set_CaretStops.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_CaretStops(self.Ptr, value)

    @property

    def DeviceFontName(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_DeviceFontName.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_DeviceFontName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_DeviceFontName(self.Ptr))
        return ret


    @DeviceFontName.setter
    def DeviceFontName(self, value:str):
        GetDllLibPdf().Glyphs_set_DeviceFontName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_DeviceFontName(self.Ptr, value)

    @property

    def Fill(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_Fill.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_Fill.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_Fill(self.Ptr))
        return ret


    @Fill.setter
    def Fill(self, value:str):
        GetDllLibPdf().Glyphs_set_Fill.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_Fill(self.Ptr, value)

    @property
    def FontRenderingEmSize(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_FontRenderingEmSize.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_FontRenderingEmSize.restype=c_double
        ret = GetDllLibPdf().Glyphs_get_FontRenderingEmSize(self.Ptr)
        return ret

    @FontRenderingEmSize.setter
    def FontRenderingEmSize(self, value:float):
        GetDllLibPdf().Glyphs_set_FontRenderingEmSize.argtypes=[c_void_p, c_double]
        GetDllLibPdf().Glyphs_set_FontRenderingEmSize(self.Ptr, value)

    @property

    def FontUri(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_FontUri.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_FontUri.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_FontUri(self.Ptr))
        return ret


    @FontUri.setter
    def FontUri(self, value:str):
        GetDllLibPdf().Glyphs_set_FontUri.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_FontUri(self.Ptr, value)

    @property
    def OriginX(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_OriginX.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_OriginX.restype=c_double
        ret = GetDllLibPdf().Glyphs_get_OriginX(self.Ptr)
        return ret

    @OriginX.setter
    def OriginX(self, value:float):
        GetDllLibPdf().Glyphs_set_OriginX.argtypes=[c_void_p, c_double]
        GetDllLibPdf().Glyphs_set_OriginX(self.Ptr, value)

    @property
    def OriginY(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_OriginY.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_OriginY.restype=c_double
        ret = GetDllLibPdf().Glyphs_get_OriginY(self.Ptr)
        return ret

    @OriginY.setter
    def OriginY(self, value:float):
        GetDllLibPdf().Glyphs_set_OriginY.argtypes=[c_void_p, c_double]
        GetDllLibPdf().Glyphs_set_OriginY(self.Ptr, value)

    @property
    def IsSideways(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_IsSideways.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_IsSideways.restype=c_bool
        ret = GetDllLibPdf().Glyphs_get_IsSideways(self.Ptr)
        return ret

    @IsSideways.setter
    def IsSideways(self, value:bool):
        GetDllLibPdf().Glyphs_set_IsSideways.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().Glyphs_set_IsSideways(self.Ptr, value)

    @property

    def Indices(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_Indices.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_Indices.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_Indices(self.Ptr))
        return ret


    @Indices.setter
    def Indices(self, value:str):
        GetDllLibPdf().Glyphs_set_Indices.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_Indices(self.Ptr, value)

    @property

    def UnicodeString(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_UnicodeString.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_UnicodeString.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_UnicodeString(self.Ptr))
        return ret


    @UnicodeString.setter
    def UnicodeString(self, value:str):
        GetDllLibPdf().Glyphs_set_UnicodeString.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_UnicodeString(self.Ptr, value)

    @property

    def StyleSimulations(self)->'StyleSimulations':
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_StyleSimulations.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_StyleSimulations.restype=c_int
        ret = GetDllLibPdf().Glyphs_get_StyleSimulations(self.Ptr)
        objwraped = StyleSimulations(ret)
        return objwraped

    @StyleSimulations.setter
    def StyleSimulations(self, value:'StyleSimulations'):
        GetDllLibPdf().Glyphs_set_StyleSimulations.argtypes=[c_void_p, c_int]
        GetDllLibPdf().Glyphs_set_StyleSimulations(self.Ptr, value.value)

    @property

    def RenderTransform(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_RenderTransform.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_RenderTransform.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_RenderTransform(self.Ptr))
        return ret


    @RenderTransform.setter
    def RenderTransform(self, value:str):
        GetDllLibPdf().Glyphs_set_RenderTransform.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_RenderTransform(self.Ptr, value)

    @property

    def Clip(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_Clip.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_Clip.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_Clip(self.Ptr))
        return ret


    @Clip.setter
    def Clip(self, value:str):
        GetDllLibPdf().Glyphs_set_Clip.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_Clip(self.Ptr, value)

    @property
    def Opacity(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_Opacity.restype=c_double
        ret = GetDllLibPdf().Glyphs_get_Opacity(self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibPdf().Glyphs_set_Opacity.argtypes=[c_void_p, c_double]
        GetDllLibPdf().Glyphs_set_Opacity(self.Ptr, value)

    @property

    def OpacityMask(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_OpacityMask.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_OpacityMask.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_OpacityMask(self.Ptr))
        return ret


    @OpacityMask.setter
    def OpacityMask(self, value:str):
        GetDllLibPdf().Glyphs_set_OpacityMask.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_OpacityMask(self.Ptr, value)

    @property

    def Name(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_Name(self.Ptr))
        return ret


    @Name.setter
    def Name(self, value:str):
        GetDllLibPdf().Glyphs_set_Name.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_Name(self.Ptr, value)

    @property

    def FixedPageNavigateUri(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_FixedPageNavigateUri.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_FixedPageNavigateUri.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_FixedPageNavigateUri(self.Ptr))
        return ret


    @FixedPageNavigateUri.setter
    def FixedPageNavigateUri(self, value:str):
        GetDllLibPdf().Glyphs_set_FixedPageNavigateUri.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_FixedPageNavigateUri(self.Ptr, value)

    @property

    def lang(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_lang.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_lang.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_lang(self.Ptr))
        return ret


    @lang.setter
    def lang(self, value:str):
        GetDllLibPdf().Glyphs_set_lang.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_lang(self.Ptr, value)

    @property

    def Key(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().Glyphs_get_Key.argtypes=[c_void_p]
        GetDllLibPdf().Glyphs_get_Key.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Glyphs_get_Key(self.Ptr))
        return ret


    @Key.setter
    def Key(self, value:str):
        GetDllLibPdf().Glyphs_set_Key.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Glyphs_set_Key(self.Ptr, value)

