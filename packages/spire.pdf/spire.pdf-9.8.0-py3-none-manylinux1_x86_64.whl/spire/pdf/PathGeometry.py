from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PathGeometry (SpireObject) :
    """
<remarks />
    """
    @property

    def PathGeometryTransform(self)->'Transform':
        """
<remarks />
        """
        GetDllLibPdf().PathGeometry_get_PathGeometryTransform.argtypes=[c_void_p]
        GetDllLibPdf().PathGeometry_get_PathGeometryTransform.restype=c_void_p
        intPtr = GetDllLibPdf().PathGeometry_get_PathGeometryTransform(self.Ptr)
        ret = None if intPtr==None else Transform(intPtr)
        return ret


    @PathGeometryTransform.setter
    def PathGeometryTransform(self, value:'Transform'):
        GetDllLibPdf().PathGeometry_set_PathGeometryTransform.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PathGeometry_set_PathGeometryTransform(self.Ptr, value.Ptr)

#    @property
#
#    def PathFigure(self)->List['PathFigure']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().PathGeometry_get_PathFigure.argtypes=[c_void_p]
#        GetDllLibPdf().PathGeometry_get_PathFigure.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PathGeometry_get_PathFigure(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, PathFigure)
#        return ret


#    @PathFigure.setter
#    def PathFigure(self, value:List['PathFigure']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().PathGeometry_set_PathFigure.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().PathGeometry_set_PathFigure(self.Ptr, vArray, vCount)


    @property

    def Figures(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().PathGeometry_get_Figures.argtypes=[c_void_p]
        GetDllLibPdf().PathGeometry_get_Figures.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PathGeometry_get_Figures(self.Ptr))
        return ret


    @Figures.setter
    def Figures(self, value:str):
        GetDllLibPdf().PathGeometry_set_Figures.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PathGeometry_set_Figures(self.Ptr, value)

    @property

    def FillRule(self)->'FillRule':
        """
<remarks />
        """
        GetDllLibPdf().PathGeometry_get_FillRule.argtypes=[c_void_p]
        GetDllLibPdf().PathGeometry_get_FillRule.restype=c_int
        ret = GetDllLibPdf().PathGeometry_get_FillRule(self.Ptr)
        objwraped = FillRule(ret)
        return objwraped

    @FillRule.setter
    def FillRule(self, value:'FillRule'):
        GetDllLibPdf().PathGeometry_set_FillRule.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PathGeometry_set_FillRule(self.Ptr, value.value)

    @property

    def Transform(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().PathGeometry_get_Transform.argtypes=[c_void_p]
        GetDllLibPdf().PathGeometry_get_Transform.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PathGeometry_get_Transform(self.Ptr))
        return ret


    @Transform.setter
    def Transform(self, value:str):
        GetDllLibPdf().PathGeometry_set_Transform.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PathGeometry_set_Transform(self.Ptr, value)

    @property

    def Key(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().PathGeometry_get_Key.argtypes=[c_void_p]
        GetDllLibPdf().PathGeometry_get_Key.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PathGeometry_get_Key(self.Ptr))
        return ret


    @Key.setter
    def Key(self, value:str):
        GetDllLibPdf().PathGeometry_set_Key.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PathGeometry_set_Key(self.Ptr, value)

