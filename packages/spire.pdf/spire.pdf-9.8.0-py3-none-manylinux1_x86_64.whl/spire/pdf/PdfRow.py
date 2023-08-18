from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfRow (SpireObject) :
    """
    <summary>
        Represents a single column of the table.
    </summary>
    """
    @property

    def Values(self)->List['SpireObject']:
        """
    <summary>
        The array of values that are used to create the new row.
    </summary>
        """
        GetDllLibPdf().PdfRow_get_Values.argtypes=[c_void_p]
        GetDllLibPdf().PdfRow_get_Values.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().PdfRow_get_Values(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, SpireObject)
        return ret

    @Values.setter
    def Values(self, value:List['SpireObject']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().PdfRow_set_Values.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().PdfRow_set_Values(self.Ptr, vArray, vCount)

