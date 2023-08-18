from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PageContent (SpireObject) :
    """
<remarks />
    """
#    @property
#
#    def PageContentLinkTargets(self)->List['LinkTarget']:
#        """
#<remarks />
#        """
#        GetDllLibPdf().PageContent_get_PageContentLinkTargets.argtypes=[c_void_p]
#        GetDllLibPdf().PageContent_get_PageContentLinkTargets.restype=IntPtrArray
#        intPtrArray = GetDllLibPdf().PageContent_get_PageContentLinkTargets(self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, LinkTarget)
#        return ret


#    @PageContentLinkTargets.setter
#    def PageContentLinkTargets(self, value:List['LinkTarget']):
#        vCount = len(value)
#        ArrayType = c_void_p * vCount
#        vArray = ArrayType()
#        for i in range(0, vCount):
#            vArray[i] = value[i].Ptr
#        GetDllLibPdf().PageContent_set_PageContentLinkTargets.argtypes=[c_void_p, ArrayType, c_int]
#        GetDllLibPdf().PageContent_set_PageContentLinkTargets(self.Ptr, vArray, vCount)


    @property

    def Source(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().PageContent_get_Source.argtypes=[c_void_p]
        GetDllLibPdf().PageContent_get_Source.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().PageContent_get_Source(self.Ptr))
        return ret


    @Source.setter
    def Source(self, value:str):
        GetDllLibPdf().PageContent_set_Source.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().PageContent_set_Source(self.Ptr, value)

    @property
    def Width(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().PageContent_get_Width.argtypes=[c_void_p]
        GetDllLibPdf().PageContent_get_Width.restype=c_double
        ret = GetDllLibPdf().PageContent_get_Width(self.Ptr)
        return ret

    @Width.setter
    def Width(self, value:float):
        GetDllLibPdf().PageContent_set_Width.argtypes=[c_void_p, c_double]
        GetDllLibPdf().PageContent_set_Width(self.Ptr, value)

    @property
    def WidthSpecified(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().PageContent_get_WidthSpecified.argtypes=[c_void_p]
        GetDllLibPdf().PageContent_get_WidthSpecified.restype=c_bool
        ret = GetDllLibPdf().PageContent_get_WidthSpecified(self.Ptr)
        return ret

    @WidthSpecified.setter
    def WidthSpecified(self, value:bool):
        GetDllLibPdf().PageContent_set_WidthSpecified.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PageContent_set_WidthSpecified(self.Ptr, value)

    @property
    def Height(self)->float:
        """
<remarks />
        """
        GetDllLibPdf().PageContent_get_Height.argtypes=[c_void_p]
        GetDllLibPdf().PageContent_get_Height.restype=c_double
        ret = GetDllLibPdf().PageContent_get_Height(self.Ptr)
        return ret

    @Height.setter
    def Height(self, value:float):
        GetDllLibPdf().PageContent_set_Height.argtypes=[c_void_p, c_double]
        GetDllLibPdf().PageContent_set_Height(self.Ptr, value)

    @property
    def HeightSpecified(self)->bool:
        """
<remarks />
        """
        GetDllLibPdf().PageContent_get_HeightSpecified.argtypes=[c_void_p]
        GetDllLibPdf().PageContent_get_HeightSpecified.restype=c_bool
        ret = GetDllLibPdf().PageContent_get_HeightSpecified(self.Ptr)
        return ret

    @HeightSpecified.setter
    def HeightSpecified(self, value:bool):
        GetDllLibPdf().PageContent_set_HeightSpecified.argtypes=[c_void_p, c_bool]
        GetDllLibPdf().PageContent_set_HeightSpecified(self.Ptr, value)

