from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class FixedDocumentSequence (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def DocumentReference(self)->List['DocumentReference']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().FixedDocumentSequence_get_DocumentReference.argtypes=[c_void_p]
#        GetDllLibPdf().FixedDocumentSequence_get_DocumentReference.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().FixedDocumentSequence_get_DocumentReference(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, DocumentReference)
#        return ret


#    @DocumentReference.setter
#    def DocumentReference(self, value:List['DocumentReference']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().FixedDocumentSequence_set_DocumentReference.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().FixedDocumentSequence_set_DocumentReference(self.Ptr, vArray, vCount)


