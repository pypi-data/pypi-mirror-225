from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfActionLinkAnnotation (  PdfLinkAnnotation) :
    """
    <summary>
        Represents base class for link annotations with associated action.
    </summary>
    """
    @property

    def Action(self)->'PdfAction':
        """
    <summary>
        Gets or sets the action for the link annotation.
    </summary>
<value>The action to be executed when the link is activated.</value>
        """
        GetDllLibPdf().PdfActionLinkAnnotation_get_Action.argtypes=[c_void_p]
        GetDllLibPdf().PdfActionLinkAnnotation_get_Action.restype=c_void_p
        intPtr = GetDllLibPdf().PdfActionLinkAnnotation_get_Action(self.Ptr)
        ret = None if intPtr==None else PdfAction(intPtr)
        return ret


    @Action.setter
    def Action(self, value:'PdfAction'):
        GetDllLibPdf().PdfActionLinkAnnotation_set_Action.argtypes=[c_void_p, c_void_p]
        GetDllLibPdf().PdfActionLinkAnnotation_set_Action(self.Ptr, value.Ptr)

