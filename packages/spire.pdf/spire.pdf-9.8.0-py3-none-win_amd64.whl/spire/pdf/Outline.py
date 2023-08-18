from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Outline (SpireObject) :
    """
<remarks />
    """
    @property

    def DocumentOutline(self)->'DocumentOutline':
        """
<remarks />
        """
        GetDllLibPdf().Outline_get_DocumentOutline.argtypes=[c_void_p]
        GetDllLibPdf().Outline_get_DocumentOutline.restype=c_void_p
        intPtr = GetDllLibPdf().Outline_get_DocumentOutline(self.Ptr)
        ret = None if intPtr==None else DocumentOutline(intPtr)
        return ret


    @DocumentOutline.setter
    def DocumentOutline(self, value:'DocumentOutline'):
        GetDllLibPdf().Outline_set_DocumentOutline.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Outline_set_DocumentOutline(self.Ptr, value.Ptr)

