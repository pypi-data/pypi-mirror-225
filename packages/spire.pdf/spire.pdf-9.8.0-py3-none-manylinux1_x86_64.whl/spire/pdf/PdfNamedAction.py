from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfNamedAction (  PdfAction) :
    """
    <summary>
        Represents an action which perfoms the named action.
    </summary>
    """
    @property

    def Destination(self)->'PdfActionDestination':
        """
    <summary>
        Gets or sets the destination.
    </summary>
<value>The  object representing destination of an action.</value>
        """
        GetDllLibPdf().PdfNamedAction_get_Destination.argtypes=[c_void_p]
        GetDllLibPdf().PdfNamedAction_get_Destination.restype=c_int
        ret = GetDllLibPdf().PdfNamedAction_get_Destination(self.Ptr)
        objwraped = PdfActionDestination(ret)
        return objwraped

    @Destination.setter
    def Destination(self, value:'PdfActionDestination'):
        GetDllLibPdf().PdfNamedAction_set_Destination.argtypes=[c_void_p, c_int]
        GetDllLibPdf().PdfNamedAction_set_Destination(self.Ptr, value.value)

