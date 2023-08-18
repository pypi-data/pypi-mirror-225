from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class MatrixTransform (SpireObject) :
    """
<remarks />
    """
    @property

    def Matrix(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().MatrixTransform_get_Matrix.argtypes=[c_void_p]
        GetDllLibPdf().MatrixTransform_get_Matrix.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().MatrixTransform_get_Matrix(self.Ptr))
        return ret


    @Matrix.setter
    def Matrix(self, value:str):
        GetDllLibPdf().MatrixTransform_set_Matrix.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().MatrixTransform_set_Matrix(self.Ptr, value)

    @property

    def Key(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().MatrixTransform_get_Key.argtypes=[c_void_p]
        GetDllLibPdf().MatrixTransform_get_Key.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().MatrixTransform_get_Key(self.Ptr))
        return ret


    @Key.setter
    def Key(self, value:str):
        GetDllLibPdf().MatrixTransform_set_Key.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().MatrixTransform_set_Key(self.Ptr, value)

