from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class FixedPage (SpireObject) :
    """
<remarks />
    """
    @property

    def FixedPageResources(self)->'Resources':
        """
<remarks />
        """
        GetDllLibPdf().FixedPage_get_FixedPageResources.argtypes=[c_void_p]
        GetDllLibPdf().FixedPage_get_FixedPageResources.restype=c_void_p
        intPtr = GetDllLibPdf().FixedPage_get_FixedPageResources(self.Ptr)
        ret = None if intPtr==None else Resources(intPtr)
        return ret


    @FixedPageResources.setter
    def FixedPageResources(self, value:'Resources'):
        GetDllLibPdf().FixedPage_set_FixedPageResources.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().FixedPage_set_FixedPageResources(self.Ptr, value.Ptr)

    @property

    def Items(self)->List['SpireObject']:
        """
<remarks />
        """
        GetDllLibPdf().FixedPage_get_Items.argtypes=[c_void_p]
        GetDllLibPdf().FixedPage_get_Items.restype=IntPtrArray
        intPtrArray = GetDllLibPdf().FixedPage_get_Items(self.Ptr)
        ret = GetVectorFromArray(intPtrArray, SpireObject)
        return ret

    @Items.setter
    def Items(self, value:List['SpireObject']):
        vCount = len(value)
        ArrayType = c_void_p * vCount
        vArray = ArrayType()
        for i in range(0, vCount):
            vArray[i] = value[i].Ptr
        GetDllLibPdf().FixedPage_set_Items.argtypes=[c_void_p, ArrayType, c_int]
        GetDllLibPdf().FixedPage_set_Items(self.Ptr, vArray, vCount)

    @property

    def Width(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().FixedPage_get_Width.argtypes=[c_void_p]
        GetDllLibPdf().FixedPage_get_Width.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().FixedPage_get_Width(self.Ptr))
        return ret


    @Width.setter
    def Width(self, value:str):
        GetDllLibPdf().FixedPage_set_Width.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().FixedPage_set_Width(self.Ptr, value)

    @property

    def Height(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().FixedPage_get_Height.argtypes=[c_void_p]
        GetDllLibPdf().FixedPage_get_Height.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().FixedPage_get_Height(self.Ptr))
        return ret


    @Height.setter
    def Height(self, value:str):
        GetDllLibPdf().FixedPage_set_Height.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().FixedPage_set_Height(self.Ptr, value)

    @property

    def ContentBox(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().FixedPage_get_ContentBox.argtypes=[c_void_p]
        GetDllLibPdf().FixedPage_get_ContentBox.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().FixedPage_get_ContentBox(self.Ptr))
        return ret


    @ContentBox.setter
    def ContentBox(self, value:str):
        GetDllLibPdf().FixedPage_set_ContentBox.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().FixedPage_set_ContentBox(self.Ptr, value)

    @property

    def BleedBox(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().FixedPage_get_BleedBox.argtypes=[c_void_p]
        GetDllLibPdf().FixedPage_get_BleedBox.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().FixedPage_get_BleedBox(self.Ptr))
        return ret


    @BleedBox.setter
    def BleedBox(self, value:str):
        GetDllLibPdf().FixedPage_set_BleedBox.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().FixedPage_set_BleedBox(self.Ptr, value)

    @property

    def lang(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().FixedPage_get_lang.argtypes=[c_void_p]
        GetDllLibPdf().FixedPage_get_lang.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().FixedPage_get_lang(self.Ptr))
        return ret


    @lang.setter
    def lang(self, value:str):
        GetDllLibPdf().FixedPage_set_lang.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().FixedPage_set_lang(self.Ptr, value)

    @property

    def Name(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().FixedPage_get_Name.argtypes=[c_void_p]
        GetDllLibPdf().FixedPage_get_Name.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().FixedPage_get_Name(self.Ptr))
        return ret


    @Name.setter
    def Name(self, value:str):
        GetDllLibPdf().FixedPage_set_Name.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().FixedPage_set_Name(self.Ptr, value)

