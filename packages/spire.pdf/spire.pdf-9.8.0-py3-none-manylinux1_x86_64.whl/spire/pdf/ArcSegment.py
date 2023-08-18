from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ArcSegment (SpireObject) :
    """
<remarks />
    """
    @property

    def Point(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().ArcSegment_get_Point.argtypes=[c_void_p]
        GetDllLibPdf().ArcSegment_get_Point.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().ArcSegment_get_Point(self.Ptr))
        return ret


    @Point.setter
    def Point(self, value:str):
        GetDllLibPdf().ArcSegment_set_Point.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().ArcSegment_set_Point(self.Ptr, value)

    @property

    def Size(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().ArcSegment_get_Size.argtypes=[c_void_p]
        GetDllLibPdf().ArcSegment_get_Size.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().ArcSegment_get_Size(self.Ptr))
        return ret


    @Size.setter
    def Size(self, value:str):
        GetDllLibPdf().ArcSegment_set_Size.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().ArcSegment_set_Size(self.Ptr, value)

    @property
    def RotationAngle(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().ArcSegment_get_RotationAngle.argtypes=[c_void_p]
        GetDllLibPdf().ArcSegment_get_RotationAngle.restype=c_double
        ret = GetDllLibPdf().ArcSegment_get_RotationAngle(self.Ptr)
        return ret

    @RotationAngle.setter
    def RotationAngle(self, value:float):
        GetDllLibPdf().ArcSegment_set_RotationAngle.argtypes=[c_void_p, c_double]
        GetDllLibPdf().ArcSegment_set_RotationAngle(self.Ptr, value)

    @property
    def IsLargeArc(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().ArcSegment_get_IsLargeArc.argtypes=[c_void_p]
        GetDllLibPdf().ArcSegment_get_IsLargeArc.restype=c_bool
        ret = GetDllLibPdf().ArcSegment_get_IsLargeArc(self.Ptr)
        return ret

    @IsLargeArc.setter
    def IsLargeArc(self, value:bool):
        GetDllLibPdf().ArcSegment_set_IsLargeArc.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().ArcSegment_set_IsLargeArc(self.Ptr, value)

    @property

    def SweepDirection(self)->'SweepDirection':
        """
<remarks />
        """
        GetDllLibPdf().ArcSegment_get_SweepDirection.argtypes=[c_void_p]
        GetDllLibPdf().ArcSegment_get_SweepDirection.restype=c_int
        ret = GetDllLibPdf().ArcSegment_get_SweepDirection(self.Ptr)
        objwraped = SweepDirection(ret)
        return objwraped

    @SweepDirection.setter
    def SweepDirection(self, value:'SweepDirection'):
        GetDllLibPdf().ArcSegment_set_SweepDirection.argtypes=[c_void_p, c_int]
        GetDllLibPdf().ArcSegment_set_SweepDirection(self.Ptr, value.value)

    @property
    def IsStroked(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().ArcSegment_get_IsStroked.argtypes=[c_void_p]
        GetDllLibPdf().ArcSegment_get_IsStroked.restype=c_bool
        ret = GetDllLibPdf().ArcSegment_get_IsStroked(self.Ptr)
        return ret

    @IsStroked.setter
    def IsStroked(self, value:bool):
        GetDllLibPdf().ArcSegment_set_IsStroked.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().ArcSegment_set_IsStroked(self.Ptr, value)

