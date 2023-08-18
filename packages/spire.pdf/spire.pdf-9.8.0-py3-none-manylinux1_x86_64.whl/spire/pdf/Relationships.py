from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Relationships (SpireObject) :
    """

    """
    @property

    def Relationship(self)->'Relationship':
        """

        """
        GetDllLibPdf().Relationships_get_Relationship.argtypes=[c_void_p]
        GetDllLibPdf().Relationships_get_Relationship.restype=c_void_p
        intPtr = GetDllLibPdf().Relationships_get_Relationship(self.Ptr)
        ret = None if intPtr==None else Relationship(intPtr)
        return ret


    @Relationship.setter
    def Relationship(self, value:'Relationship'):
        GetDllLibPdf().Relationships_set_Relationship.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Relationships_set_Relationship(self.Ptr, value.Ptr)

