from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PathFigure (SpireObject) :
    """
<remarks />
    """
    @property

    def Items(self)->List['SpireObject']:
        """
<remarks />
        """
        GetDllLibPdf().PathFigure_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().PathFigure_get_Items.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PathFigure_get_Items(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, SpireObject)
        return ret

    @Items.setter
    def Items(self, value:List['SpireObject']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().PathFigure_set_Items.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PathFigure_set_Items(self.Ptr, vArray, vCount)

    @property
    def IsClosed(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().PathFigure_get_IsClosed.argtypes=[c_void_p]
        GetDllLibPdf().PathFigure_get_IsClosed.restype=c_bool
        ret = GetDllLibPdf().PathFigure_get_IsClosed(self.Ptr)
        return ret

    @IsClosed.setter
    def IsClosed(self, value:bool):
        GetDllLibPdf().PathFigure_set_IsClosed.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PathFigure_set_IsClosed(self.Ptr, value)

    @property

    def StartPoint(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().PathFigure_get_StartPoint.argtypes=[c_void_p]
        GetDllLibPdf().PathFigure_get_StartPoint.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PathFigure_get_StartPoint(self.Ptr))
        return ret


    @StartPoint.setter
    def StartPoint(self, value:str):
        GetDllLibPdf().PathFigure_set_StartPoint.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PathFigure_set_StartPoint(self.Ptr, value)

    @property
    def IsFilled(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().PathFigure_get_IsFilled.argtypes=[c_void_p]
        GetDllLibPdf().PathFigure_get_IsFilled.restype=c_bool
        ret = GetDllLibPdf().PathFigure_get_IsFilled(self.Ptr)
        return ret

    @IsFilled.setter
    def IsFilled(self, value:bool):
        GetDllLibPdf().PathFigure_set_IsFilled.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PathFigure_set_IsFilled(self.Ptr, value)

