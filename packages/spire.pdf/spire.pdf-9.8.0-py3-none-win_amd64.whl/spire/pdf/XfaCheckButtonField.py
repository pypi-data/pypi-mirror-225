from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XfaCheckButtonField (  XfaField) :
    """

    """
#    @property
#
#    def Items(self)->'List1':
#        """
#
#        """
#        GetDllLibPdf().XfaCheckButtonField_get_Items.argtypes=[c_void_p]
#        GetDllLibPdf().XfaCheckButtonField_get_Items.restype=c_void_p
#        intPtr = GetDllLibPdf().XfaCheckButtonField_get_Items(self.Ptr)
#        ret = None if intPtr==None else List1(intPtr)
#        return ret
#


    @property
    def Checked(self)->bool:
        """

        """
        GetDllLibPdf().XfaCheckButtonField_get_Checked.argtypes=[c_void_p]
        GetDllLibPdf().XfaCheckButtonField_get_Checked.restype=c_bool
        ret = GetDllLibPdf().XfaCheckButtonField_get_Checked(self.Ptr)
        return ret

    @Checked.setter
    def Checked(self, value:bool):
        GetDllLibPdf().XfaCheckButtonField_set_Checked.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().XfaCheckButtonField_set_Checked(self.Ptr, value)

