from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PolyQuadraticBezierSegment (SpireObject) :
    """
<remarks />
    """
    @property

    def Points(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().PolyQuadraticBezierSegment_get_Points.argtypes=[c_void_p]
        GetDllLibPdf().PolyQuadraticBezierSegment_get_Points.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PolyQuadraticBezierSegment_get_Points(self.Ptr))
        return ret


    @Points.setter
    def Points(self, value:str):
        GetDllLibPdf().PolyQuadraticBezierSegment_set_Points.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PolyQuadraticBezierSegment_set_Points(self.Ptr, value)

    @property
    def IsStroked(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().PolyQuadraticBezierSegment_get_IsStroked.argtypes=[c_void_p]
        GetDllLibPdf().PolyQuadraticBezierSegment_get_IsStroked.restype=c_bool
        ret = GetDllLibPdf().PolyQuadraticBezierSegment_get_IsStroked(self.Ptr)
        return ret

    @IsStroked.setter
    def IsStroked(self, value:bool):
        GetDllLibPdf().PolyQuadraticBezierSegment_set_IsStroked.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PolyQuadraticBezierSegment_set_IsStroked(self.Ptr, value)

