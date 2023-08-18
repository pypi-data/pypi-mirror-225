from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class XmpSchema (  XmpEntityBase) :
    """

    """
    @property

    def SchemaType(self)->'XmpSchemaType':
        """

        """
        GetDllLibPdf().XmpSchema_get_SchemaType.argtypes=[c_void_p]
        GetDllLibPdf().XmpSchema_get_SchemaType.restype=c_int
        ret = GetDllLibPdf().XmpSchema_get_SchemaType(self.Ptr)
        objwraped = XmpSchemaType(ret)
        return objwraped


    def CreateStructure(self ,type:'XmpStructureType')->'XmpStructure':
        """

        """
        enumtype:c_int = type.value

        GetDllLibPdf().XmpSchema_CreateStructure.argtypes=[c_void_p ,c_int]
        GetDllLibPdf().XmpSchema_CreateStructure.restype=c_void_p
        intPtr = GetDllLibPdf().XmpSchema_CreateStructure(self.Ptr, enumtype)
        ret = None if intPtr==None else XmpStructure(intPtr)
        return ret


