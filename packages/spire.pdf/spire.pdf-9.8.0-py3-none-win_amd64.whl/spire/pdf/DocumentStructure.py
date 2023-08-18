from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class DocumentStructure (SpireObject) :
    """
<remarks />
    """
    @property

    def DocumentStructureOutline(self)->'Outline':
        """
<remarks />
        """
        GetDllLibPdf().DocumentStructure_get_DocumentStructureOutline.argtypes=[c_void_p]
        GetDllLibPdf().DocumentStructure_get_DocumentStructureOutline.restype=c_void_p
        intPtr = GetDllLibPdf().DocumentStructure_get_DocumentStructureOutline(self.Ptr)
        ret = None if intPtr==None else Outline(intPtr)
        return ret


    @DocumentStructureOutline.setter
    def DocumentStructureOutline(self, value:'Outline'):
        GetDllLibPdf().DocumentStructure_set_DocumentStructureOutline.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().DocumentStructure_set_DocumentStructureOutline(self.Ptr, value.Ptr)

#    @property
#
#    def Story(self)->List['Story']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().DocumentStructure_get_Story.argtypes=[c_void_p]
#        GetDllLibPdf().DocumentStructure_get_Story.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().DocumentStructure_get_Story(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, Story)
#        return ret


#    @Story.setter
#    def Story(self, value:List['Story']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().DocumentStructure_set_Story.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().DocumentStructure_set_Story(self.Ptr, vArray, vCount)


