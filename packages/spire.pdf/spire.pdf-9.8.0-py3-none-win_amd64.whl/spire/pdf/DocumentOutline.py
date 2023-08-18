from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class DocumentOutline (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def OutlineEntry(self)->List['OutlineEntry']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().DocumentOutline_get_OutlineEntry.argtypes=[c_void_p]
#        GetDllLibPdf().DocumentOutline_get_OutlineEntry.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().DocumentOutline_get_OutlineEntry(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, OutlineEntry)
#        return ret


#    @OutlineEntry.setter
#    def OutlineEntry(self, value:List['OutlineEntry']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().DocumentOutline_set_OutlineEntry.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().DocumentOutline_set_OutlineEntry(self.Ptr, vArray, vCount)


    @property

    def lang(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().DocumentOutline_get_lang.argtypes=[c_void_p]
        GetDllLibPdf().DocumentOutline_get_lang.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().DocumentOutline_get_lang(self.Ptr))
        return ret


    @lang.setter
    def lang(self, value:str):
        GetDllLibPdf().DocumentOutline_set_lang.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().DocumentOutline_set_lang(self.Ptr, value)

