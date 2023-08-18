from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Brush (SpireObject) :
    """
<remarks />
    """
    @property

    def Item(self)->'SpireObject':
        """
<remarks />
        """
        GetDllLibPdf().Brush_get_Item.argtypes=[c_void_p]
        GetDllLibPdf().Brush_get_Item.restype=c_void_p
        intPtr = GetDllLibPdf().Brush_get_Item(self.Ptr)
        ret = None if intPtr==None else SpireObject(intPtr)
        return ret


    @Item.setter
    def Item(self, value:'SpireObject'):
        GetDllLibPdf().Brush_set_Item.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().Brush_set_Item(self.Ptr, value.Ptr)

