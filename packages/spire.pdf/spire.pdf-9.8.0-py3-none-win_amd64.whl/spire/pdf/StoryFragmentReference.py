from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class StoryFragmentReference (SpireObject) :
    """
<remarks />
    """
    @property

    def FragmentName(self)->str:
        """
<remarks />
        """
        GetDllLibPdf().StoryFragmentReference_get_FragmentName.argtypes=[c_void_p]
        GetDllLibPdf().StoryFragmentReference_get_FragmentName.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().StoryFragmentReference_get_FragmentName(self.Ptr))
        return ret


    @FragmentName.setter
    def FragmentName(self, value:str):
        GetDllLibPdf().StoryFragmentReference_set_FragmentName.argtypes=[c_void_p, c_wchar_p]
        GetDllLibPdf().StoryFragmentReference_set_FragmentName(self.Ptr, value)

    @property
    def Page(self)->int:
        """
<remarks />
        """
        GetDllLibPdf().StoryFragmentReference_get_Page.argtypes=[c_void_p]
        GetDllLibPdf().StoryFragmentReference_get_Page.restype=c_int
        ret = GetDllLibPdf().StoryFragmentReference_get_Page(self.Ptr)
        return ret

    @Page.setter
    def Page(self, value:int):
        GetDllLibPdf().StoryFragmentReference_set_Page.argtypes=[c_void_p, c_int]
        GetDllLibPdf().StoryFragmentReference_set_Page(self.Ptr, value)

