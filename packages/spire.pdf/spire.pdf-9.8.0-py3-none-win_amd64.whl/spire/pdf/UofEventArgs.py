from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class UofEventArgs (SpireObject) :
    """
    <summary>
        The event arguments passed between TranslatorLib and Add-in
    </summary>
<author>linwei</author>
    """
    @property

    def Message(self)->str:
        """

        """
        GetDllLibPdf().UofEventArgs_get_Message.argtypes=[c_void_p]
        GetDllLibPdf().UofEventArgs_get_Message.restype=c_void_p
        ret = PtrToStr(GetDllLibPdf().UofEventArgs_get_Message(self.Ptr))
        return ret


