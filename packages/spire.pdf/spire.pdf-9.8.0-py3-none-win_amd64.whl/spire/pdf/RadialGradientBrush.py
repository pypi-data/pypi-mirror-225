from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class RadialGradientBrush (SpireObject) :
    """
<remarks />
    """
    @property

    def RadialGradientBrushTransform(self)->'Transform':
        """
<remarks />
        """
        GetDllLibPdf().RadialGradientBrush_get_RadialGradientBrushTransform.argtypes=[c_void_p]
        GetDllLibPdf().RadialGradientBrush_get_RadialGradientBrushTransform.restype=c_void_p
        intPtr = GetDllLibPdf().RadialGradientBrush_get_RadialGradientBrushTransform(self.Ptr)
        ret = None if intPtr==None else Transform(intPtr)
        return ret


    @RadialGradientBrushTransform.setter
    def RadialGradientBrushTransform(self, value:'Transform'):
        GetDllLibPdf().RadialGradientBrush_set_RadialGradientBrushTransform.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().RadialGradientBrush_set_RadialGradientBrushTransform(self.Ptr, value.Ptr)

#    @property
#
#    def RadialGradientBrushGradientStops(self)->List['GradientStop']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().RadialGradientBrush_get_RadialGradientBrushGradientStops.argtypes=[c_void_p]
#        GetDllLibPdf().RadialGradientBrush_get_RadialGradientBrushGradientStops.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().RadialGradientBrush_get_RadialGradientBrushGradientStops(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, GradientStop)
#        return ret


#    @RadialGradientBrushGradientStops.setter
#    def RadialGradientBrushGradientStops(self, value:List['GradientStop']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().RadialGradientBrush_set_RadialGradientBrushGradientStops.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().RadialGradientBrush_set_RadialGradientBrushGradientStops(self.Ptr, vArray, vCount)


    @property
    def Opacity(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().RadialGradientBrush_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().RadialGradientBrush_get_Opacity.restype=c_double
        ret = GetDllLibPdf().RadialGradientBrush_get_Opacity(self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibPdf().RadialGradientBrush_set_Opacity.argtypes=[c_void_p, c_double]
        GetDllLibPdf().RadialGradientBrush_set_Opacity(self.Ptr, value)

    @property

    def Key(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().RadialGradientBrush_get_Key.argtypes=[c_void_p]
        GetDllLibPdf().RadialGradientBrush_get_Key.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().RadialGradientBrush_get_Key(self.Ptr))
        return ret


    @Key.setter
    def Key(self, value:str):
        GetDllLibPdf().RadialGradientBrush_set_Key.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().RadialGradientBrush_set_Key(self.Ptr, value)

    @property

    def ColorInterpolationMode(self)->'ClrIntMode':
        """
<remarks />
        """
        GetDllLibPdf().RadialGradientBrush_get_ColorInterpolationMode.argtypes=[c_void_p]
        GetDllLibPdf().RadialGradientBrush_get_ColorInterpolationMode.restype=c_int
        ret = GetDllLibPdf().RadialGradientBrush_get_ColorInterpolationMode(self.Ptr)
        objwraped = ClrIntMode(ret)
        return objwraped

    @ColorInterpolationMode.setter
    def ColorInterpolationMode(self, value:'ClrIntMode'):
        GetDllLibPdf().RadialGradientBrush_set_ColorInterpolationMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().RadialGradientBrush_set_ColorInterpolationMode(self.Ptr, value.value)

    @property

    def SpreadMethod(self)->'SpreadMethod':
        """
<remarks />
        """
        GetDllLibPdf().RadialGradientBrush_get_SpreadMethod.argtypes=[c_void_p]
        GetDllLibPdf().RadialGradientBrush_get_SpreadMethod.restype=c_int
        ret = GetDllLibPdf().RadialGradientBrush_get_SpreadMethod(self.Ptr)
        objwraped = SpreadMethod(ret)
        return objwraped

    @SpreadMethod.setter
    def SpreadMethod(self, value:'SpreadMethod'):
        GetDllLibPdf().RadialGradientBrush_set_SpreadMethod.argtypes=[c_void_p, c_int]
        GetDllLibPdf().RadialGradientBrush_set_SpreadMethod(self.Ptr, value.value)

    @property

    def MappingMode(self)->'MappingMode':
        """
<remarks />
        """
        GetDllLibPdf().RadialGradientBrush_get_MappingMode.argtypes=[c_void_p]
        GetDllLibPdf().RadialGradientBrush_get_MappingMode.restype=c_int
        ret = GetDllLibPdf().RadialGradientBrush_get_MappingMode(self.Ptr)
        objwraped = MappingMode(ret)
        return objwraped

    @MappingMode.setter
    def MappingMode(self, value:'MappingMode'):
        GetDllLibPdf().RadialGradientBrush_set_MappingMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().RadialGradientBrush_set_MappingMode(self.Ptr, value.value)

    @property

    def Transform(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().RadialGradientBrush_get_Transform.argtypes=[c_void_p]
        GetDllLibPdf().RadialGradientBrush_get_Transform.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().RadialGradientBrush_get_Transform(self.Ptr))
        return ret


    @Transform.setter
    def Transform(self, value:str):
        GetDllLibPdf().RadialGradientBrush_set_Transform.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().RadialGradientBrush_set_Transform(self.Ptr, value)

    @property

    def Center(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().RadialGradientBrush_get_Center.argtypes=[c_void_p]
        GetDllLibPdf().RadialGradientBrush_get_Center.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().RadialGradientBrush_get_Center(self.Ptr))
        return ret


    @Center.setter
    def Center(self, value:str):
        GetDllLibPdf().RadialGradientBrush_set_Center.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().RadialGradientBrush_set_Center(self.Ptr, value)

    @property

    def GradientOrigin(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().RadialGradientBrush_get_GradientOrigin.argtypes=[c_void_p]
        GetDllLibPdf().RadialGradientBrush_get_GradientOrigin.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().RadialGradientBrush_get_GradientOrigin(self.Ptr))
        return ret


    @GradientOrigin.setter
    def GradientOrigin(self, value:str):
        GetDllLibPdf().RadialGradientBrush_set_GradientOrigin.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().RadialGradientBrush_set_GradientOrigin(self.Ptr, value)

    @property
    def RadiusX(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().RadialGradientBrush_get_RadiusX.argtypes=[c_void_p]
        GetDllLibPdf().RadialGradientBrush_get_RadiusX.restype=c_double
        ret = GetDllLibPdf().RadialGradientBrush_get_RadiusX(self.Ptr)
        return ret

    @RadiusX.setter
    def RadiusX(self, value:float):
        GetDllLibPdf().RadialGradientBrush_set_RadiusX.argtypes=[c_void_p, c_double]
        GetDllLibPdf().RadialGradientBrush_set_RadiusX(self.Ptr, value)

    @property
    def RadiusY(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().RadialGradientBrush_get_RadiusY.argtypes=[c_void_p]
        GetDllLibPdf().RadialGradientBrush_get_RadiusY.restype=c_double
        ret = GetDllLibPdf().RadialGradientBrush_get_RadiusY(self.Ptr)
        return ret

    @RadiusY.setter
    def RadiusY(self, value:float):
        GetDllLibPdf().RadialGradientBrush_set_RadiusY.argtypes=[c_void_p, c_double]
        GetDllLibPdf().RadialGradientBrush_set_RadiusY(self.Ptr, value)

