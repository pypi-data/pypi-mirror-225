from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XfaBarcodeField (  XfaField) :
    """

    """
    @property
    def Length(self)->int:
        """

        """
        GetDllLibPdf().XfaBarcodeField_get_Length.argtypes=[c_void_p]
        GetDllLibPdf().XfaBarcodeField_get_Length.restype=c_int
        ret = GetDllLibPdf().XfaBarcodeField_get_Length(self.Ptr)
        return ret

    @Length.setter
    def Length(self, value:int):
        GetDllLibPdf().XfaBarcodeField_set_Length.argtypes=[c_void_p, c_int]
        GetDllLibPdf().XfaBarcodeField_set_Length(self.Ptr, value)

    @property

    def Value(self)->str:
        """

        """
        GetDllLibPdf().XfaBarcodeField_get_Value.argtypes=[c_void_p]
        GetDllLibPdf().XfaBarcodeField_get_Value.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XfaBarcodeField_get_Value(self.Ptr))
        return ret


    @Value.setter
    def Value(self, value:str):
        GetDllLibPdf().XfaBarcodeField_set_Value.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().XfaBarcodeField_set_Value(self.Ptr, value)

    @property
    def StartChar(self)->int:
        """

        """
        GetDllLibPdf().XfaBarcodeField_get_StartChar.argtypes=[c_void_p]
        GetDllLibPdf().XfaBarcodeField_get_StartChar.restype=c_int
        ret = GetDllLibPdf().XfaBarcodeField_get_StartChar(self.Ptr)
        return ret

    @StartChar.setter
    def StartChar(self, value:int):
        GetDllLibPdf().XfaBarcodeField_set_StartChar.argtypes=[c_void_p, c_int]
        GetDllLibPdf().XfaBarcodeField_set_StartChar(self.Ptr, value)

    @property
    def EndChar(self)->int:
        """

        """
        GetDllLibPdf().XfaBarcodeField_get_EndChar.argtypes=[c_void_p]
        GetDllLibPdf().XfaBarcodeField_get_EndChar.restype=c_int
        ret = GetDllLibPdf().XfaBarcodeField_get_EndChar(self.Ptr)
        return ret

    @EndChar.setter
    def EndChar(self, value:int):
        GetDllLibPdf().XfaBarcodeField_set_EndChar.argtypes=[c_void_p, c_int]
        GetDllLibPdf().XfaBarcodeField_set_EndChar(self.Ptr, value)

