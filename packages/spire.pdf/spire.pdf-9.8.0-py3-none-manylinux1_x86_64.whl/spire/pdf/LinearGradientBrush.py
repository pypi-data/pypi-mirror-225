from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class LinearGradientBrush (SpireObject) :
    """
<remarks />
    """
    @property

    def LinearGradientBrushTransform(self)->'Transform':
        """
<remarks />
        """
        GetDllLibPdf().LinearGradientBrush_get_LinearGradientBrushTransform.argtypes=[c_void_p]
        GetDllLibPdf().LinearGradientBrush_get_LinearGradientBrushTransform.restype=c_void_p
        intPtr = GetDllLibPdf().LinearGradientBrush_get_LinearGradientBrushTransform(self.Ptr)
        ret = None if intPtr==None else Transform(intPtr)
        return ret


    @LinearGradientBrushTransform.setter
    def LinearGradientBrushTransform(self, value:'Transform'):
        GetDllLibPdf().LinearGradientBrush_set_LinearGradientBrushTransform.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().LinearGradientBrush_set_LinearGradientBrushTransform(self.Ptr, value.Ptr)

#    @property
#
#    def LinearGradientBrushGradientStops(self)->List['GradientStop']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().LinearGradientBrush_get_LinearGradientBrushGradientStops.argtypes=[c_void_p]
#        GetDllLibPdf().LinearGradientBrush_get_LinearGradientBrushGradientStops.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().LinearGradientBrush_get_LinearGradientBrushGradientStops(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, GradientStop)
#        return ret


#    @LinearGradientBrushGradientStops.setter
#    def LinearGradientBrushGradientStops(self, value:List['GradientStop']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().LinearGradientBrush_set_LinearGradientBrushGradientStops.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().LinearGradientBrush_set_LinearGradientBrushGradientStops(self.Ptr, vArray, vCount)


    @property
    def Opacity(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().LinearGradientBrush_get_Opacity.argtypes=[c_void_p]
        GetDllLibPdf().LinearGradientBrush_get_Opacity.restype=c_double
        ret = GetDllLibPdf().LinearGradientBrush_get_Opacity(self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibPdf().LinearGradientBrush_set_Opacity.argtypes=[c_void_p, c_double]
        GetDllLibPdf().LinearGradientBrush_set_Opacity(self.Ptr, value)

    @property

    def Key(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().LinearGradientBrush_get_Key.argtypes=[c_void_p]
        GetDllLibPdf().LinearGradientBrush_get_Key.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().LinearGradientBrush_get_Key(self.Ptr))
        return ret


    @Key.setter
    def Key(self, value:str):
        GetDllLibPdf().LinearGradientBrush_set_Key.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().LinearGradientBrush_set_Key(self.Ptr, value)

    @property

    def ColorInterpolationMode(self)->'ClrIntMode':
        """
<remarks />
        """
        GetDllLibPdf().LinearGradientBrush_get_ColorInterpolationMode.argtypes=[c_void_p]
        GetDllLibPdf().LinearGradientBrush_get_ColorInterpolationMode.restype=c_int
        ret = GetDllLibPdf().LinearGradientBrush_get_ColorInterpolationMode(self.Ptr)
        objwraped = ClrIntMode(ret)
        return objwraped

    @ColorInterpolationMode.setter
    def ColorInterpolationMode(self, value:'ClrIntMode'):
        GetDllLibPdf().LinearGradientBrush_set_ColorInterpolationMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().LinearGradientBrush_set_ColorInterpolationMode(self.Ptr, value.value)

    @property

    def SpreadMethod(self)->'SpreadMethod':
        """
<remarks />
        """
        GetDllLibPdf().LinearGradientBrush_get_SpreadMethod.argtypes=[c_void_p]
        GetDllLibPdf().LinearGradientBrush_get_SpreadMethod.restype=c_int
        ret = GetDllLibPdf().LinearGradientBrush_get_SpreadMethod(self.Ptr)
        objwraped = SpreadMethod(ret)
        return objwraped

    @SpreadMethod.setter
    def SpreadMethod(self, value:'SpreadMethod'):
        GetDllLibPdf().LinearGradientBrush_set_SpreadMethod.argtypes=[c_void_p, c_int]
        GetDllLibPdf().LinearGradientBrush_set_SpreadMethod(self.Ptr, value.value)

    @property

    def MappingMode(self)->'MappingMode':
        """
<remarks />
        """
        GetDllLibPdf().LinearGradientBrush_get_MappingMode.argtypes=[c_void_p]
        GetDllLibPdf().LinearGradientBrush_get_MappingMode.restype=c_int
        ret = GetDllLibPdf().LinearGradientBrush_get_MappingMode(self.Ptr)
        objwraped = MappingMode(ret)
        return objwraped

    @MappingMode.setter
    def MappingMode(self, value:'MappingMode'):
        GetDllLibPdf().LinearGradientBrush_set_MappingMode.argtypes=[c_void_p, c_int]
        GetDllLibPdf().LinearGradientBrush_set_MappingMode(self.Ptr, value.value)

    @property

    def Transform(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().LinearGradientBrush_get_Transform.argtypes=[c_void_p]
        GetDllLibPdf().LinearGradientBrush_get_Transform.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().LinearGradientBrush_get_Transform(self.Ptr))
        return ret


    @Transform.setter
    def Transform(self, value:str):
        GetDllLibPdf().LinearGradientBrush_set_Transform.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().LinearGradientBrush_set_Transform(self.Ptr, value)

    @property

    def StartPoint(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().LinearGradientBrush_get_StartPoint.argtypes=[c_void_p]
        GetDllLibPdf().LinearGradientBrush_get_StartPoint.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().LinearGradientBrush_get_StartPoint(self.Ptr))
        return ret


    @StartPoint.setter
    def StartPoint(self, value:str):
        GetDllLibPdf().LinearGradientBrush_set_StartPoint.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().LinearGradientBrush_set_StartPoint(self.Ptr, value)

    @property

    def EndPoint(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().LinearGradientBrush_get_EndPoint.argtypes=[c_void_p]
        GetDllLibPdf().LinearGradientBrush_get_EndPoint.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().LinearGradientBrush_get_EndPoint(self.Ptr))
        return ret


    @EndPoint.setter
    def EndPoint(self, value:str):
        GetDllLibPdf().LinearGradientBrush_set_EndPoint.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().LinearGradientBrush_set_EndPoint(self.Ptr, value)

