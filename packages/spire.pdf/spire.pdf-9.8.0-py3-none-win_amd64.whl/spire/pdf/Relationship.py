from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Relationship (SpireObject) :
    """

    """
    @property

    def Type(self)->str:
        """

        """
        GetDllLibPdf().Relationship_get_Type.argtypes=[c_void_p]
        GetDllLibPdf().Relationship_get_Type.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Relationship_get_Type(self.Ptr))
        return ret


    @Type.setter
    def Type(self, value:str):
        GetDllLibPdf().Relationship_set_Type.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Relationship_set_Type(self.Ptr, value)

    @property

    def Target(self)->str:
        """

        """
        GetDllLibPdf().Relationship_get_Target.argtypes=[c_void_p]
        GetDllLibPdf().Relationship_get_Target.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Relationship_get_Target(self.Ptr))
        return ret


    @Target.setter
    def Target(self, value:str):
        GetDllLibPdf().Relationship_set_Target.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Relationship_set_Target(self.Ptr, value)

    @property

    def Id(self)->str:
        """

        """
        GetDllLibPdf().Relationship_get_Id.argtypes=[c_void_p]
        GetDllLibPdf().Relationship_get_Id.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().Relationship_get_Id(self.Ptr))
        return ret


    @Id.setter
    def Id(self, value:str):
        GetDllLibPdf().Relationship_set_Id.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().Relationship_set_Id(self.Ptr, value)

