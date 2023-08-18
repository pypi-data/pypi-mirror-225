from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfAction (SpireObject) :
    """
    <summary>
        Represents base class for all action types.
    </summary>
    """
    @property

    def NextAction(self)->'PdfAction':
        """
    <summary>
        Gets or sets the next action to be performed after the action represented by this instance.
    </summary>
        """
        GetDllLibPdf().PdfAction_get_NextAction.argtypes=[c_void_p]
        GetDllLibPdf().PdfAction_get_NextAction.restype=c_void_p
        intPtr = GetDllLibPdf().PdfAction_get_NextAction(self.Ptr)
        ret = None if intPtr==None else PdfAction(intPtr)
        return ret


    @NextAction.setter
    def NextAction(self, value:'PdfAction'):
        GetDllLibPdf().PdfAction_set_NextAction.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfAction_set_NextAction(self.Ptr, value.Ptr)

