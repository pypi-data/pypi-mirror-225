from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class FixedDocument (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def PageContent(self)->List['PageContent']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().FixedDocument_get_PageContent.argtypes=[c_void_p]
#        GetDllLibPdf().FixedDocument_get_PageContent.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().FixedDocument_get_PageContent(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, PageContent)
#        return ret


#    @PageContent.setter
#    def PageContent(self, value:List['PageContent']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().FixedDocument_set_PageContent.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().FixedDocument_set_PageContent(self.Ptr, vArray, vCount)


    @property

    def DocumentReferenceRoot(self)->str:
        """

        """
        GetDllLibPdf().FixedDocument_get_DocumentReferenceRoot.argtypes=[c_void_p]
        GetDllLibPdf().FixedDocument_get_DocumentReferenceRoot.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().FixedDocument_get_DocumentReferenceRoot(self.Ptr))
        return ret


    @DocumentReferenceRoot.setter
    def DocumentReferenceRoot(self, value:str):
        GetDllLibPdf().FixedDocument_set_DocumentReferenceRoot.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().FixedDocument_set_DocumentReferenceRoot(self.Ptr, value)

