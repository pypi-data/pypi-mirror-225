from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class SignatureDefinitionsType (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def SignatureDefinition(self)->List['SignatureDefinitionType']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().SignatureDefinitionsType_get_SignatureDefinition.argtypes=[c_void_p]
#        GetDllLibPdf().SignatureDefinitionsType_get_SignatureDefinition.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().SignatureDefinitionsType_get_SignatureDefinition(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, SignatureDefinitionType)
#        return ret


#    @SignatureDefinition.setter
#    def SignatureDefinition(self, value:List['SignatureDefinitionType']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().SignatureDefinitionsType_set_SignatureDefinition.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().SignatureDefinitionsType_set_SignatureDefinition(self.Ptr, vArray, vCount)


