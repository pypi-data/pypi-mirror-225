from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XfaField (SpireObject) :
    """

    """
    @property

    def Name(self)->str:
        """

        """
        GetDllLibPdf().XfaField_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().XfaField_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XfaField_get_Name(self.Ptr))
        return ret


    @property

    def XfaForm(self)->'XFAForm':
        """

        """
        GetDllLibPdf().XfaField_get_XfaForm.argtypes=[c_void_p]
        GetDllLibPdf().XfaField_get_XfaForm.restype=c_void_p
        intPtr = GetDllLibPdf().XfaField_get_XfaForm(self.Ptr)
        ret = None if intPtr==None else XFAForm(intPtr)
        return ret


    @property

    def FieldType(self)->str:
        """

        """
        GetDllLibPdf().XfaField_get_FieldType.argtypes=[c_void_p]
        GetDllLibPdf().XfaField_get_FieldType.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().XfaField_get_FieldType(self.Ptr))
        return ret


