from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Resources (SpireObject) :
    """
<remarks />
    """
    @property

    def ResourceDictionary(self)->'ResourceDictionary':
        """
<remarks />
        """
        GetDllLibPdf().Resources_get_ResourceDictionary.argtypes=[c_void_p]
        GetDllLibPdf().Resources_get_ResourceDictionary.restype=c_void_p
        intPtr = GetDllLibPdf().Resources_get_ResourceDictionary(self.Ptr)
        ret = None if intPtr==None else ResourceDictionary(intPtr)
        return ret


    @ResourceDictionary.setter
    def ResourceDictionary(self, value:'ResourceDictionary'):
        GetDllLibPdf().Resources_set_ResourceDictionary.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Resources_set_ResourceDictionary(self.Ptr, value.Ptr)

